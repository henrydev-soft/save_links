"""
En este archivo se define la clase con las variables de configuración de la aplicación. 
Utiliza pydantic para cargar los valores desde un archivo .env o desde variables de entorno.
"""

import os
from pydantic_settings  import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache
from pathlib import Path
from typing import Optional


def get_env_file_path() -> Optional[Path]:
    """
    Retorna la ruta del archivo .env si no se está en Docker.
    Si se detecta que estamos dentro de Docker (por una variable), retorna None.
    """
    if os.getenv("RUNNING_IN_DOCKER") == "true":
        return None  # No cargar archivo .env
    # En local: buscar el .env en la raíz del proyecto
    return Path(__file__).resolve().parents[2] / ".env"

env_path = get_env_file_path()

class Settings(BaseSettings):
    APP_NAME: str = "Course Manager"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PROJECT_VERSION: str = "1.0.0"

    FIREBASE_CREDENTIALS_PATH: str = "path/to/credentials.json"    

    model_config = ConfigDict(
        env_file=get_env_file_path(),
        env_file_encoding="utf-8"
    )

#Función que agregar el cache de la instancia para evitar múltiples lecturas del archivo .env
@lru_cache
def get_settings() -> Settings:
    return Settings()