"""
Servicios de aplicación

Este paquete contiene los servicios encargados de la lógica de aplicación
(casos de uso), que se ubican entre la capa de interfaces (controladores/API)
y la capa de dominio (modelos y repositorios).

Responsabilidades:
- Coordinar operaciones del dominio.
- Orquestar validaciones de negocio.
- Transformar o adaptar datos entre capas.

Servicios incluidos:
- `link_service.py`: operaciones sobre enlaces.
- `user_service.py`: operaciones sobre usuarios.

Autor: Henry Jiménez
Fecha: 2025-06-11
"""

from .link_service import LinkService
#from .user_service import UserService

__all__ = ["LinkService"]