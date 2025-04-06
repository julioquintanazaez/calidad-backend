from typing import Union, Optional, List
from datetime import date
from pydantic import BaseModel, EmailStr 

	
class User_Read(BaseModel):	
	usuario: str	
	role: List[str] = ["admin", "usuario"]
	class Config:
		from_attributes = True
		populate_by_name = True
		arbitrary_types_allowed = True	

class User_Record(User_Read):
	hashed_password: str
	
class User_InDB(User_Record):
	id: str

class User_Activate(BaseModel):	
	deshabilitado: Union[bool, None] = None
		
class User_ResetPassword(BaseModel):
	newpassword: str