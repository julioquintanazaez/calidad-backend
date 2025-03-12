from typing import Union, Optional, List
from datetime import date
from pydantic import BaseModel, EmailStr 

class ModeloCalidadAdd(BaseModel):
	nombre_modelo : str
	desc_modelo : str
	tipo_modelo : str

	class Config:
		from_attributes = True
		populate_by_name = True
		arbitrary_types_allowed = True	

class ModeloCalidadDB(ModeloCalidadAdd):	
	id_modelo : str	


	