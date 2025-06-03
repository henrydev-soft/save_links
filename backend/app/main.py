"""Este es el archivo principal de la aplicación FastAPI."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.settings import settings
from .core.firebase_config import initialize_firebase

from .db.base import Base
from .db.session import engine
from .api.v1.routes import links

#Crear las tablas en la base de datos al iniciar la aplicación
Base.metadata.create_all(bind=engine)

app = FastAPI()

#Inicializar Firebase Admin SDK
initialize_firebase()

# Configurar CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI application!"}


#Incluir las rutas de la API
app.include_router(links.router, prefix="/api/v1/links")