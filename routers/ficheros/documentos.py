from fastapi import APIRouter, Depends, UploadFile, Form, File, HTTPException, status, Security
from fastapi.responses import FileResponse, Response, StreamingResponse
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine, get_db
from models import data
from schemas import documentos
from security.auth import get_current_active_user, get_current_user
from typing_extensions import Annotated
from schemas.user import User_InDB
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import os
import core.config as config
import mimetypes

router = APIRouter()

@router.post("/files/", response_model=documentos.TextFile)
async def create_file(
    current_user: Annotated[User_InDB, Security(get_current_user, scopes=["admin"])],
    name: str=Form(...),
    description: str=Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Guardar el archivo físicamente
    file_path = os.path.join(config.UPLOAD_DIR, file.filename)
    
    # Verificar si el archivo ya existe
    if os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="El fichero ya esta almacenado en la base de datos")
    
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Guardar en la base de datos
    db_file = data.TextFile(
        name=name,
        description=description,
        file_path=file_path
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    return db_file

@router.get("/files/", response_model=list[documentos.TextFile])
def read_files(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    files = db.query(data.TextFile).offset(skip).limit(limit).all()
    return files

@router.get("/files/{file_id}", response_model=documentos.TextFile)
def read_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(data.TextFile).filter(data.TextFile.id == file_id).first()
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file

@router.delete("/files/{file_id}/delete")
def delete_file(
                #current_user: Annotated[User_InDB, Security(get_current_user, scopes=["admin"])],
                file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(data.TextFile).filter(data.TextFile.id == file_id).first()
    if db_file is None or not os.path.exists(db_file.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    os.remove(db_file.file_path)
    db.delete(db_file)	
    db.commit()
    return {"Remove": True}
    

@router.get("/files/{file_id}/download")
def download_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(data.TextFile).filter(data.TextFile.id == file_id).first()
    if db_file is None or not os.path.exists(db_file.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    #print(db_file.file_path)
    real_file_path = db_file.file_path.split("/")
    file_path = real_file_path[len(real_file_path)-1]
    mime_type, _ = mimetypes.guess_type(file_path)
    print(mime_type)
    media_type = mime_type or "application/octet-stream" # 
    response = FileResponse(db_file.file_path, media_type=media_type)
    response.headers["Content-Disposition"] = f"attachment; filename*=utf-8''{file_path}" #filename*=utf-8''
    return response
    