"""
Mapper para la entidad Link

Autor: Henry Jiménez
Fecha: 2025-06-11
"""

from app.domain.models import Link, NewLink
from app.application.dtos import LinkRead, LinkCreate, LinkUpdate

class LinkMapper:
    
    @staticmethod
    def create_entity_from_dto(link_create_dto: LinkCreate, user_id: str) -> NewLink:
        """ Mapea un DTO de creación de enlace a una entidad de enlace."""
        return NewLink(
            url=link_create_dto.url,
            title=link_create_dto.title,
            description=link_create_dto.description,
            user_id=user_id,
            tags=link_create_dto.tags if link_create_dto.tags is not None else []
        )
    
    @staticmethod
    def update_entity_from_dto(existing: Link, link_update_dto: LinkUpdate) -> Link:
        """ Mapea un DTO de actualización de enlace a una entidad de enlace."""
        return Link(
            id=existing.id,
            url=link_update_dto.url if link_update_dto.url is not None else existing.url,
            title=link_update_dto.title if link_update_dto.title is not None else existing.title,
            description=link_update_dto.description if link_update_dto.description is not None else existing.description,
            created_at=existing.created_at,
            tags =  link_update_dto.tags if link_update_dto.tags is not None else existing.tags,
            user_id=existing.user_id
        )
    
    @staticmethod
    def entity_to_dto(link: Link) -> LinkRead:
        """ Mapea una entidad de enlace a un DTO de lectura."""
        return LinkRead(
            id=link.id,
            url=link.url,
            title=link.title,
            description=link.description,
            tags=link.tags,
            user_id=link.user_id,
            created_at=link.created_at
        )