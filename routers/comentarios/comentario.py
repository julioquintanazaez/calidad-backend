from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.responses import StreamingResponse
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
from wordcloud import WordCloud
import io
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

router = APIRouter()

@router.post("/comentario/", status_code=status.HTTP_201_CREATED)
async def crear_comentario(input_coment: comentarios.ComentarioBase,
						    db: Session = Depends(get_db)):
	
	resultado = analyzer.polarity_scores(input_coment.comentario)
	del resultado["compound"]
	final_thought = dict(sorted(resultado.items(), key=lambda item: item[1], reverse=True))
	final_thought = list(final_thought.items())[0]
	final_thought = final_thought[0] + "_" + str(final_thought[1])

	try:
		db_comentario = data.Comentarios(
			comentario = input_coment.comentario,
			documento_id = input_coment.documento_id,
			pensamiento = final_thought,
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

@router.delete("/comentario/delete-items/")
async def delete_items(request: comentarios.DeleteRequest, db: Session = Depends(get_db)):
    parent_index = request.documento_id
    indices_to_delete = request.indices
    # Verificar si el padre existe
    parent = db.query(data.TextFile).filter(data.TextFile.id == parent_index).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent index not found")
    # Si el documento padre existe, Eliminar los elementos
    items_to_delete = db.query(data.Comentarios).filter(
		data.Comentarios.documento_id == parent_index,
		data.Comentarios.id_comentario.in_(indices_to_delete)).all()
    if not items_to_delete:
        raise HTTPException(status_code=404, detail="No items found to delete")
    for item in items_to_delete:
        db.delete(item)
    db.commit()
    return {"message": "Comentarios eliminados satisfactoriamente"}

@router.get("/comentario/wordcloud/", status_code=status.HTTP_201_CREATED)  
async def crear_wordcloud(current_user: Annotated[User_InDB, Security(get_current_user, scopes=["admin"])],
					db: Session = Depends(get_db)):    
	db_comentarios = db.query(data.Comentarios).all()
	texto = ""
	for comentario in db_comentarios:
		texto = texto + ". " + comentario.comentario
	wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto)
    # Guardar la imagen en un objeto BytesIO
	img_stream = io.BytesIO()
	wordcloud.to_image().save(img_stream, format='PNG')
	img_stream.seek(0)  # Volver al inicio del flujo
	return StreamingResponse(img_stream, media_type='image/png', headers={"Content-Disposition": "attachment; filename=wordcloud.png"})

@router.get("/comentario/sumario/", status_code=status.HTTP_201_CREATED)  
async def hacer_resumen(current_user: Annotated[User_InDB, Security(get_current_user, scopes=["admin"])],
					db: Session = Depends(get_db)):    
	db_comentarios = db.query(data.Comentarios).all()
	texto = ""
	for comentario in db_comentarios:
		texto = texto + ". " + comentario.comentario
	
	

	# Obtener la polaridad
	resultado = analyzer.polarity_scores(texto)
	

	del resultado["compound"]
	final_thought = dict(sorted(resultado.items(), key=lambda item: item[1], reverse=True))
	final_thought = list(final_thought.items())[0]
	final_thought = final_thought[0] + "_" + str(final_thought[1])
	print(final_thought)
	return {"res": final_thought}
