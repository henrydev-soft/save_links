"""
Mappers de aplicación

El objetivo de los mapper es convertir entre entidades de dominio a DTOs y viceversa,
facilitando la comunicación entre la capa de dominio y la capa de presentación.

Actualmente se encuentran definidos los mappers para las entidades:

- UserMapper: Mapea entre User y UserRead.
- LinkMapper: Mapea entre Link y LinkRead.

Autor: Henry Jiménez
Fecha: 2025-06-11
"""

from .link_mapper import LinkMapper
from .user_mapper import UserMapper

__all__ = ["LinkMapper", "UserMapper"]
