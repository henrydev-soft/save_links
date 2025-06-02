"""Este es el archivo principal de la aplicación FastAPI."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db.base import Base
from .db.session import engine

from .api.v1.routes import links

from .core.config import CORS_ALLOW_ORIGINS, CORS_ALLOW_CREDENTIALS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS

#Crear las tablas en la base de datos al iniciar la aplicación
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurar CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI application!"}


#Incluir las rutas de la API
app.include_router(links.router, prefix="/api/v1/links")