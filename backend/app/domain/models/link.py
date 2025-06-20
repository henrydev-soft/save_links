"""
Link Entity

Este módulo define la entidad de dominio `Link`. Esta entidad es utilizada en la capa de dominio 
y no depende de frameworks externos como ORMs o librerías de serialización.

Responsabilidades:
- Encapsular la estructura de datos de un curso.
- Actuar como modelo base en los servicios de aplicación y repositorios.

Autor: Henry Jiménez
Fecha: 2025-06-16
"""

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Link:
    """
    Clase que representa un enlace almacenado.

    Atributos:
        id (str): Identificador único del enlace.
        title (str): Título del enlace.
        description (str): Descripción del enlace.
        created_at (str): Fecha de creación del enlace en formato ISO 8601.
        user_id (str): Identificador del usuario propietario del enlace.
        tags (List[str]): Lista de etiquetas asociadas al enlace.
    """
    id: str
    title: str
    url: str
    description: str
    created_at: str
    user_id: str
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.id or not self.title or not self.url or not self.user_id:
            raise ValueError("id, title, url,  and user_id cannot be empty")

@dataclass
class NewLink:
    """
    Clase que representa los datos necesarios para crear un nuevo enlace.

    Atributos:
        title (str): Título del enlace.
        description (str): Descripción del enlace.
        user_id (str): Identificador del usuario propietario del enlace.
        tags (List[str]): Lista de etiquetas asociadas al enlace.
    """
    title: str
    url: str
    user_id: str
    description: Optional[str] = None    
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.title or not self.url or not self.user_id:
            raise ValueError("title, url and user_id cannot be empty")