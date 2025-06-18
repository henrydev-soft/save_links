"""
Mapper para la entidad User

Autor: Henry Jiménez
Fecha: 2025-06-11
"""

from app.domain.models import User
from app.application.dtos import UserRead, UserCreate, UserUpdate


class UserMapper:
    
    @staticmethod
    def create_entity_from_dto(user_create_dto: UserCreate) -> User:
        """ Mapea un DTO de creación de usuario a una entidad de usuario."""
        return User(
            email=user_create_dto.email,
            username=user_create_dto.username,
        )
    
    
    def update_entity_from_dto(user_update_dto: UserUpdate) -> User:
        """ Mapea un DTO de actualización de usuario a una entidad de usuario."""
        return User(
            email=user_update_dto.email,
            username=user_update_dto.username,
        )
    
    def entity_to_dto(user: User) -> UserRead:
        """ Mapea una entidad de usuario a un DTO de lectura de usuario."""
        return UserRead(
            id=user.id,
            email=user.email,
            username=user.username,
        )