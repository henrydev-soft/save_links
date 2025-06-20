"""
Rutas de la API versión 1

Este subpaquete agrupa las rutas organizadas por entidad (
y define los endpoints específicos para cada recurso.

Cada módulo contiene:
- Métodos HTTP REST (GET, POST, PUT, DELETE).
- Lógica mínima de enrutamiento.
- Inyección de dependencias que delegan a servicios de aplicación.

Archivos incluidos:
- `link.py`: CRUD de enlaces.
- `user.py`: CRUD de usuarios.

Autor: Henry Jiménez
Fecha: 2025-06-19
"""

from .user import router as user_router
from .link import router as link_router