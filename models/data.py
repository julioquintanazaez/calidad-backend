#from db.database import Base
import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Float, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from sqlalchemy.types import TypeDecorator, String
from sqlalchemy.sql import func
import json
from uuid import UUID, uuid4 
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class JSONEncodeDict(TypeDecorator):
	impl = String	
	def process_bind_param(self, value, dialect):
		if value is not None:
			value = json.dumps(value)
		return value
	
	def process_result_value(self, value, dialect):
		if value is not None:
			value = json.loads(value)
		return value
		
class User(Base):
	__tablename__ = "user"
	
	id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE, index=True)
	usuario = Column(String(30), unique=True, index=True) 
	role = Column(JSONEncodeDict)
	hashed_password = Column(String(100), nullable=True, default=False)	

class TextFile(Base):
	__tablename__ = "text_files"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String(100), index=True)
	description = Column(Text, nullable=True)
	file_path = Column(String(255), unique=True)
	comentarios_documentos = relationship("Comentarios", back_populates="documentos", cascade="all, delete")


class Comentarios(Base):
	__tablename__ = "comentarios"

	id_comentario = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE, index=True)
	comentario = Column(String(300), index=True)
	fecha_comentario = Column(DateTime, nullable=False, server_default=func.now())

	documento_id = Column(Integer, ForeignKey("text_files.id"))
	documentos = relationship("TextFile", back_populates="comentarios_documentos")	

