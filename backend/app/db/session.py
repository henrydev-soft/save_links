"""
Este módulo contiene la configuración para la conexión a la base de datos SQLite y la 
función para obtener la sesión de la base de datos como dependencia de FastAPI.
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL


engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Crea una sesión de base de datos y la devuelve como dependencia de FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()