"""
Esquemas para el modelo de enlace (Link) en la aplicación FastAPI.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class LinkBase(BaseModel):
    """
    Esquema base para un enlace.
    Contiene los campos comunes a todos los enlaces.
    """
    url: str
    title: Optional[str] = None
    description: Optional[str] = None


class LinkCreate(LinkBase):
    """
    Esquema para crear un nuevo enlace.
    Hereda de LinkBase y no añade campos adicionales.
    """
    pass

class LinkUpdate(LinkBase):
    """
    Esquema para actualizar un enlace existente.
    Hereda de LinkBase y no añade campos adicionales.
    """
    pass

class Link(LinkBase):
    """
    Esquema para representar un enlace completo.
    Hereda de LinkBase e incluye el campo 'id' y 'created_at'.
    """
    id: int
    created_at: datetime
    owner_uid: str
    model_config = ConfigDict(from_attributes=True)