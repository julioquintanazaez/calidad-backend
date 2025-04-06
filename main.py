from fastapi import FastAPI
from functools import lru_cache
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
import os

import core.config as config
from routers.user import users
from routers.security import auth
from routers.ficheros import documentos
from routers.comentarios import comentario

#Create our main app
app = FastAPI()

app.include_router(auth.router)  #, prefix="/auth", tags=["auth"]
app.include_router(users.router, prefix="/usuario", tags=["usuario"])
app.include_router(documentos.router, prefix="/documents", tags=["documents"])
app.include_router(comentario.router, prefix="/comentarios", tags=["comentario"])

# Allow these methods to be used
methods = ["GET", "POST", "PUT", "DELETE"]

# Only these headers are allowed
headers = ["Content-Type", "Authorization"]

app.add_middleware(
	CORSMiddleware,
	allow_origins=config.CORS_ORIGINS,
	allow_credentials=True,
	allow_methods=methods,
	allow_headers=headers,
	expose_headers=["*"]
)

os.makedirs(config.UPLOAD_DIR, exist_ok=True)

@app.get("/")
def index():
	return {"Aplicación": "Sistema de recomendación de productos hoteleros"}
	
