"""
Link DTOs

Este módulo contiene los modelos Pydantic que actúan como Data Transfer Objects (DTOs)
para la entidad Link. Su propósito es definir claramente las estructuras utilizadas
para recibir y devolver datos relacionados con lecciones en la API REST.

Modelos definidos:
- LinkBase: Modelo base con los campos comunes.
- LinkCreate: Modelo para crear nuevos enlaces (POST).
- LinkUpdate: Modelo para modificar datos de un enlace existente (PUT).
- LinkRead: Modelo para representar un enlace al ser leido desde la API (GET).

Los DTOs permiten desacoplar las estructuras de datos de la lógica de negocio
y del ORM, promoviendo un diseño limpio y mantenible.

Autor: Henry Jiménez
Fecha: 2025-06-16
"""

from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime

from app.core import app_validator


class LinkBase(BaseModel):
    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[str] = None
    created_at: Optional[datetime] = None
    tags = Optional[list[str]] = None

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        return app_validator.is_valid_url(v)

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        return app_validator.check_length("title", v, 100, 3)

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        return app_validator.check_length("description", v, 500, 3)


class LinkCreate(LinkBase):
    url: str
    title: str
    description: str
    created_at: datetime
    
class LinkUpdate(LinkBase):
    pass

class LinkRead(LinkBase):
    id: str
    url: str
    title: str
    description: str    
    user_id: str
    created_at: datetime
    tags: list[str]