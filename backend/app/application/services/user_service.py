"""
Servicio de aplicación para la entidad User

Este servicio implementa la lógica de negocio para gestionar enlaces
de un usuario. Maneja operaciones de creación, actualización, consulta
y eliminación, con validaciones de dominio y control de errores.

Autor: Henry Jiménez
Fecha: 2025-06-11
"""

from app.domain.models import User
from app.domain.repositories import IUserRepository
from app.application.mappers import UserMapper
from app.application.dtos import UserCreate, UserUpdate, UserRead
from app.core.exceptions import UserNotFoundException
from app.core import logger


class UserService:
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def _get_user_or_raise(self, user_id: str) -> User:
        """ Metodo privado responsable de obtener el usuario o lanzar una excepcion en caso de no encontrarlo """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        return user

    
    def get_user_by_id(self, user_id: str) -> UserRead:
        """ Retorna la información de un usuario por su ID."""
        
        logger.info(f"Obteniendo información del usuario con ID: {user_id}")
        user = self._get_user_or_raise(user_id)        
        logger.info(f"Usuario Encontrado")
        
        return UserMapper.entity_to_dto(user)
    
    def create_user(self, user_create: UserCreate) -> UserRead:
        """ Crea un nuevo usuario en el repositorio."""
        
        logger.info(f"Creando nuevo usuario con ID: {user_create.id}")
        user = UserMapper.create_entity_from_dto(user_create)
        user = self.user_repository.create(user)
        logger.info(f"Usuario creado con ID: {user.id}")
        
        return UserMapper.entity_to_dto(user)

    def update_user(self, user_id: str, user_update: UserUpdate) -> UserRead:
        """ Actualiza un usuario existente en el repositorio."""
        
        logger.info(f"Actualizando usuario con ID: {user_id}")
        user = self._get_user_or_raise(user_id)
        user = UserMapper.update_entity_from_dto(user, user_update)
        user = self.user_repository.update(user)
        logger.info(f"Usuario actualizado con ID: {user.id}")
        
        return UserMapper.entity_to_dto(user)
    
    def delete_user(self, user_id: str) -> None:
        """ Elimina un usuario existente en el repositorio."""
        
        logger.info(f"Eliminando usuario con ID: {user_id}")
        self._get_user_or_raise(user_id)
        self.user_repository.delete(user_id)
        logger.info(f"Usuario eliminado con ID: {user_id}")