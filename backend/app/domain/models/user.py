"""
User Entity

Este módulo define la entidad de dominio `User`. Esta entidad es utilizada en la 
capa de dominio y no depende de frameworks externos como ORMs o librerías de serialización.

Responsabilidades:
- Encapsular la estructura de datos de un curso.
- Actuar como modelo base en los servicios de aplicación y repositorios.

Autor: Henry Jiménez
Fecha: 2025-06-16
"""

from dataclasses import dataclass, field
from typing import List, Optional
from .link import Link

@dataclass
class User:
    """
    Clase que representa un usuario del sistema.

    Atributos:
        id (str): Identificador único del usuario.
        email (str): Correo electrónico del usuario.
        name (str): Nombre del usuario.
        links (List[str]): Lista de enlaces asociados al usuario.
    """
    id: str
    email: str
    name: str
    links: List[Link] = field(default_factory=list)

    def __post_init__(self):
        if not self.id or not self.email or not self.name:
            raise ValueError("id, email, and name cannot be empty")