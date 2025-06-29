"""
Servicio de aplicación para la entidad Link

Este servicio implementa la lógica de negocio para gestionar enlaces
de un usuario. Maneja operaciones de creación, actualización, consulta
y eliminación, con validaciones de dominio y control de errores.

Autor: Henry Jiménez
Fecha: 2025-06-11
"""

from typing import List
from app.domain.models import Link, User
from app.domain.repositories import ILinkRepository, IUserRepository
from app.application.dtos import LinkCreate, LinkUpdate, LinkRead
from app.application.mappers import LinkMapper
from app.core.exceptions import LinkNotFoundException, UserNotFoundException, PermissionException
from app.core import logger


class LinkService:
    def __init__(self, link_repository: ILinkRepository, user_repository: IUserRepository):
        self.link_repository = link_repository
        self.user_repository = user_repository
    
    def __validate_user_data(self, user_data: dict, user_id: str) -> None:
        """ Valida que el usuario autenticado coincida con los datos del usuario."""
        if user_data["uid"] != user_id:
            raise PermissionException()
        
    def _get_user_or_raise(self, user_id: str) -> User:
        """ Metodo privado responsable de obtener el usuario o lanzar una excepcion en caso de no encontrarlo """
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        return user

    def _get_link_or_raise(self, link_id: str) -> Link:
        """ Metodo privado responsable de obtener el link o lanzar una excepcion en caso de no encontrarlo """
        link = self.link_repository.get_link_by_id(link_id)
        if not link:
            raise LinkNotFoundException(link_id)
        return link
    
    def _ensure_ownership(self,  user_id: str, link_id: str) -> Link:
        """ Metodo privado que verifica la pertenencia del link al usuario autenticado """
        link = self._get_link_or_raise(link_id)
        if link.user_id != user_id:
            raise PermissionException()
        return link
    
    def get_links_by_user_id(self, user_id: str, user_data: dict) -> List[LinkRead]:
        """Obtiene todos los enlaces asociados a un usuario."""
        
        logger.info(f"Obteniendo enlaces para usuario: {user_id}")
        
        self.__validate_user_data(user_data, user_id)
        self._get_user_or_raise(user_id)       
        links = self.link_repository.get_links_by_user_id(user_id)
        
        logger.info(f"Enlaces obtenidos para usuario: {user_id}")
        return [LinkMapper.entity_to_dto(link) for link in links]
    
    def create_link(self, link_create: LinkCreate, user_id: str, user_data: dict) -> LinkRead:
        """Crea un nuevo enlace para el usuario autenticado."""
        
        logger.info(f"Creando enlace para usuario: {user_id}")
        self.__validate_user_data(user_data, user_id)
        self._get_user_or_raise(user_id)              
        new_link = LinkMapper.create_entity_from_dto(link_create, user_id)
        link_create = self.link_repository.create_link(new_link)
        
        logger.info(f"Enlace creado ID=%S:",link_create.id)
                    
        return LinkMapper.entity_to_dto(link_create)

    def update_link(self, user_id: str, link_id: str, link_update: LinkUpdate, user_data: dict) -> LinkRead:
        """Actualiza un enlace existente."""
        
        logger.info(f"Actualizando Enlace ID=%s:", link_id)
        self.__validate_user_data(user_data, user_id)
        existing_link = self._ensure_ownership(user_id, link_id)    
        updated_entity = LinkMapper.update_entity_from_dto(existing_link, link_update)
        link_update = self.link_repository.update_link(updated_entity)
        
        logger.info(f"Enlace actualizado con ID=%s:", link_id)
        
        return LinkMapper.entity_to_dto(link_update)

    
    def delete_link(self, user_id: str, link_id: str, user_data: dict) -> None:
        """Elimina un enlace."""
        
        logger.info(f"Eliminando Enlace ID=%s:", link_id)
        
        self.__validate_user_data(user_data, user_id)
        link = self._ensure_ownership(user_id,link_id)
        self.link_repository.delete_link(link.id)
        
        logger.info(f"Enlace eliminado con ID=%s:", link_id)