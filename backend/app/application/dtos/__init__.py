"""
Paquete de Data Transfer Objects (DTOs)

Este paquete contiene los modelos Pydantic utilizados para la validación, serialización
y deserialización de datos en la comunicación entre la API (interfaces) y la capa de 
aplicación.

Los DTOs definen estructuras claras para:
- Entrada de datos (crear/actualizar entidades).
- Salida de datos (lectura y respuesta al cliente).

Cada módulo dentro del paquete corresponde a una entidad del dominio, e incluye
modelos específicos para los diferentes tipos de operación: creación, lectura,
actualización.

DTOs definidos:
- `user.py`: modelos relacionados con la entidad User.
- `link.py`: modelos relacionados con la entidad Link.

Este enfoque ayuda a mantener una separación clara entre la lógica de negocio
(modelos de dominio), la infraestructura (ORM) y la presentación (API).

Autor: Henry Jiménez
Fecha: 2025-06-16
"""

from .link import LinkCreate, LinkUpdate, LinkRead
from .user import UserCreate, UserUpdate, UserRead

__all__ = [
    "LinkCreate",
    "LinkUpdate",
    "LinkRead",
    "UserCreate",
    "UserUpdate",
    "UserRead",
]