from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine, get_db
from models.data import Modelos_Calidad
from schemas.modeloscalidad import ModeloCalidadAdd, ModeloCalidadDB
from security.auth import get_current_active_user, get_current_user
from typing_extensions import Annotated
from schemas.user import User_InDB
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

router = APIRouter()

"""
@router.post("/crear_modelo/", status_code=status.HTTP_201_CREATED)
async def crear_servicio(current_user: Annotated[User_InDB, Security(get_current_user, scopes=["admin"])],
					nuevo_modelo: ModeloCalidadAdd, db: Session = Depends(get_db)):
	try:
		db_servicio = Servicio(
			nombre_modelo = nuevo_modelo.nombre_servicio,
			desc_servicio = nuevo_servicio.desc_servicio, 
			tipo_servicio = nuevo_servicio.tipo_servicio			
		)			
		db.add(db_servicio)   	
		db.commit()
		db.refresh(db_servicio)			
		return db_servicio
	except IntegrityError as e:
		raise HTTPException(status_code=500, detail="Error de integridad creando objeto Servicio")
	except SQLAlchemyError as e: 
		raise HTTPException(status_code=405, detail="Error SQLAlchemy creando el objeto Servicio")		


@router.get("/leer_servicios/", status_code=status.HTTP_201_CREATED)  
async def leer_servicios(current_user: Annotated[User_InDB, Security(get_current_user, scopes=["trabajador"])],
					skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):    
		return db.query(Servicio).offset(skip).limit(limit).all() 
		

@router.delete("/eliminar_servicio/{id}", status_code=status.HTTP_201_CREATED) 
async def eliminar_servicio(current_user: Annotated[User_InDB, Security(get_current_user, scopes=["admin"])],
					id: str, db: Session = Depends(get_db)):
	db_servicio = db.query(Servicio).filter(Servicio.id_servicio == id).first()
	if db_servicio is None:
		raise HTTPException(status_code=404, detail="El servicio no existe en la base de datos")	
	db.delete(db_servicio)	
	db.commit()
	return {"Result": "Servicio eliminado satisfactoriamente"}

"""
@router.put("/actualizar_modelo/{id}", status_code=status.HTTP_201_CREATED) 
async def actualizar_modelo(current_user: Annotated[User_InDB, Security(get_current_user, scopes=["admin"])], 
				id: str, modelo: ModeloCalidadAdd, db: Session = Depends(get_db)):
	db_modelo = db.query(Modelos_Calidad).filter(Modelos_Calidad.id_modelo == id).first()
	if db_modelo is None:
		raise HTTPException(status_code=404, detail="El modelo seleccionado no existen en la base de datos")
	db_modelo.nombre_modelo = modelo.nombre_modelo
	db_modelo.desc_modelo = modelo.desc_modelo
	db_modelo.tipo_modelo = modelo.tipo_modelo
	db.commit()
	db.refresh(db_modelo)	
	return {"Result": "Datos del modelo actualizados satisfactoriamente"}	
	


