"""
Archivo de configuración para la aplicación FastAPI.
Este archivo contiene la configuración de la aplicación, incluyendo la URL de la base de datos,
y la configuración de CORS (Cross-Origin Resource Sharing).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./app.db"

    # Configuración de CORS
    CORS_ALLOW_ORIGINS: list[str] = ["http://localhost:4200"] # Permitir todas los orígenes
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    # Configuración de Firebase
    FIREBASE_SERVICE_ACCOUNT_KEY_PATH: Optional[str] = None # Nuevo campo para la ruta del archivo JSON

    model_config = SettingsConfigDict(env_file=".env") # Esto carga variables del .env

settings = Settings()