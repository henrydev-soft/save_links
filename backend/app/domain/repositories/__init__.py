"""
Interfaces de repositorios del dominio

Este paquete contiene las interfaces (puertos de salida) que definen cómo debe accederse
a los datos de las entidades del dominio desde la perspectiva de la lógica de negocio.

Estas interfaces no contienen detalles técnicos de persistencia, y permiten
desacoplar los servicios de aplicación de cualquier implementación concreta (como una base de datos NoSQL).

Interfaces definidas:
- ILinkRepository: interfaz para operaciones sobre enlaces.
- IUserRepository: interfaz para operaciones sobre usuarios.

Sus implementaciones concretas se encuentran en `infrastructure/repositories/`.

Autor: Henry Jiménez
Fecha: 2025-06-16
"""

from .link_repository import ILinkRepository
from .user_repository import IUserRepository

__all__ = ["ILinkRepository", "IUserRepository"]