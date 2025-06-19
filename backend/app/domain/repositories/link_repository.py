"""
Interfaz del repositorio de Link

Define los métodos necesarios para gestionar la persistencia de objetos tipo `Link`.
Esta interfaz debe ser implementada por una clase concreta (por ejemplo, usando NoSQL).

Permite desacoplar la lógica de aplicación del mecanismo específico de almacenamiento
siguiendo los principios de inversión de dependencias y arquitectura hexagonal.

Autor: Henry Jiménez
Fecha: 2025-06-16
"""

from abc import ABC, abstractmethod
from typing import List
from app.domain.models import Link, NewLink

class ILinkRepository(ABC):
    """
    Interfaz del repositorio de links.
    
    Define los métodos necesarios para gestionar la persistencia de objetos tipo `Link`.
    Esta interfaz debe ser implementada por una clase concreta (por ejemplo, usando NoSQL).
    
    Permite desacoplar la lógica de aplicación del mecanismo específico de almacenamiento
    siguiendo los principios de inversión de dependencias y arquitectura hexagonal.
    """

    @abstractmethod
    def create_link(self, link: NewLink) -> Link:
        """Crea un nuevo enlace en el repositorio."""
        pass

    @abstractmethod
    def get_links_by_user_id(self, user_id: str) -> List[Link]:
        """Obtiene todos los enlaces asociados a un usuario."""
        pass

    @abstractmethod
    def update_link(self, link: Link) -> Link:
        """Actualiza un enlace existente."""
        pass

    @abstractmethod
    def delete_link(self, link_id: str) -> None:
        """Elimina un enlace por su identificador."""
        pass