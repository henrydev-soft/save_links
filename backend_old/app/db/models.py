"""
Este módulo define la clase base para los modelos de SQLAlchemy.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from .base import Base

class Link(Base):
    """
    Modelo de SQLAlchemy para la tabla 'links'.
    Representa un enlace con un ID, URL, título, descripción y fecha de creación.
    """
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True, nullable=False)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    owner_uid = Column(String, index=True, nullable=False)
    
    def __repr__(self):
        return f"<Link(id={self.id}, url={self.url}, title={self.title})>"