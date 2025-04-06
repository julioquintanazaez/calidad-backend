from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine, get_db
from models import data
from schemas import comentarios
from security.auth import get_current_active_user, get_current_user
from typing_extensions import Annotated
from schemas.user import User_InDB
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import joinedload
#import pandas as pd
from core import config

router = APIRouter()

@router.post("/comentario/", status_code=status.HTTP_201_CREATED)
async def crear_comentario(input_coment: comentarios.ComentarioBase,
						    db: Session = Depends(get_db)):
	try:
		db_comentario = data.Comentarios(
			comentario = input_coment.comentario,
			documento_id = input_coment.documento_id
		)			
		db.add(db_comentario)   	
		db.commit()
		db.refresh(db_comentario)			
		return db_comentario
	except IntegrityError as e:
		raise HTTPException(status_code=500, detail="Error de integridad creando el comentario") #
	except SQLAlchemyError as e: 
		raise HTTPException(status_code=405, detail="Error SQLAlchemy creando el comentario")		


@router.delete("/comentario/delete/{id}", status_code=status.HTTP_201_CREATED) 
async def eliminar_comentario(current_user: Annotated[User_InDB, Security(get_current_user, scopes=["admin"])],
					id: str, db: Session = Depends(get_db)):
	db_comentario = db.query(data.Comentarios).filter(data.Comentarios.id_comentario == id).first()
	if db_comentario is None:
		raise HTTPException(status_code=404, detail="El comentario no existe en la base de datos")	
	db.delete(db_comentario)	
	db.commit()
	return {"Result": "Comentario eliminado satisfactoriamente"}


@router.get("/comentario/{id}/todos", status_code=status.HTTP_201_CREATED)  
async def leer_comentarios(current_user: Annotated[User_InDB, Security(get_current_user, scopes=["admin"])],
					id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):    
	
	return db.query(data.Comentarios).filter(data.Comentarios.documento_id == id).all()

@router.get("/comentario/sumario", status_code=status.HTTP_201_CREATED)  
async def sumario_comentarios(current_user: Annotated[User_InDB, Security(get_current_user, scopes=["admin"])],
					db: Session = Depends(get_db)):    
	
    db_comentarios = db.query(data.Comentarios).all()
    for comentario in db_comentarios:
        print(comentario.comentario)
		
    return {"Res": True}


