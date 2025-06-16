"""
Interfaz del repositorio de User

Define los métodos necesarios para gestionar la persistencia de objetos tipo `User`.
Esta interfaz debe ser implementada por una clase concreta (por ejemplo, usando NoSQL).

Permite desacoplar la lógica de aplicación del mecanismo específico de almacenamiento
siguiendo los principios de inversión de dependencias y arquitectura hexagonal.

Autor: Henry Jiménez
Fecha: 2025-06-16
"""


from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models import User

class IUserRepository(ABC):
    """
    Interfaz del repositorio de User.
    
    Define los métodos necesarios para gestionar la persistencia de objetos tipo `User`.
    Esta interfaz debe ser implementada por una clase concreta (por ejemplo, usando NoSQL).
    
    Permite desacoplar la lógica de aplicación del mecanismo específico de almacenamiento
    siguiendo los principios de inversión de dependencias y arquitectura hexagonal.
    """

    @abstractmethod
    def create(self, user: User) -> User:
        """Crea un nuevo usuario en el repositorio."""
        pass

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Obtiene un usuario por su identificador."""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Actualiza un usuario existente."""
        pass
    
    @abstractmethod
    def delete(self, user_id: str)-> None:
        """Elimina un usuario por su identificador."""
        pass