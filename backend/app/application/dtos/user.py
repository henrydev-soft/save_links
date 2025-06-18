"""
User DTOs

Este módulo contiene los modelos Pydantic que actúan como Data Transfer Objects (DTOs)
para la entidad User. Su propósito es definir claramente las estructuras utilizadas
para recibir y devolver datos relacionados con lecciones en la API REST.

Modelos definidos:
- UserBase: Modelo base con los campos comunes.
- UserCreate: Modelo para crear nuevos usuarios (POST).
- UserUpdate: Modelo para modificar datos de un usuario existente (PUT).
- UserRead: Modelo para representar un usuario al ser leido desde la API (GET).

Los DTOs permiten desacoplar las estructuras de datos de la lógica de negocio
y del ORM, promoviendo un diseño limpio y mantenible.

Autor: Henry Jiménez
Fecha: 2025-06-16
"""


from typing import Optional
from pydantic import BaseModel, field_validator

from app.core import app_validator



class UserBase(BaseModel):
    id: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    
    @field_validator("email")
    def validate_email(cls, v: str):
        return app_validator.is_valid_email(v)
    
    @field_validator("username")
    def validate_username(cls, v: str):
        return app_validator.check_length("username", v, 50, 3)


class UserCreate(UserBase):
    id: str
    email: str
    username: str
    
class UserUpdate(UserBase):
    pass

class UserRead(UserBase):
    id: str
    email: str
    username: str