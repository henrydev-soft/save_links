"""
Paquete de modelos del dominio

Este paquete contiene las entidades centrales del dominio de la aplicación, como `User` y `Link`.
Estas clases representan conceptos del negocio de forma pura, sin depender de frameworks externos
como ORMs, APIs o serializadores.

Los modelos del dominio son utilizados por los servicios de aplicación y repositorios como
fuente de verdad para las reglas de negocio, garantizando una separación clara respecto
a la infraestructura y a la capa de presentación.

Entidades definidas:
- Link: representa un recurso virtual.
- User: representa un usuario del sistema.

Autor: Henry Jiménez
Fecha: 2025-06-16
"""

from .user import User
from .link import Link, NewLink

__all__ = ["User", "Link", "NewLink"]