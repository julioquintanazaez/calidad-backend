from typing import Union, Optional, List
from datetime import date
from pydantic import BaseModel, EmailStr 

class ComentarioBase(BaseModel):		
	comentario : str 
	documento_id : int
	
	class Config:
		from_attributes = True
		populate_by_name = True
		arbitrary_types_allowed = True	

class ComentarioDB(ComentarioBase):		
	id_comentario : str
	fecha_comentario : date

class DeleteRequest(BaseModel):
    indices: List[str]
    documento_id: int

	
