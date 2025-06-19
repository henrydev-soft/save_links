"""
Rutas HTTP para la gestión de enlaces

Define los endpoints REST para crear, actualizar, eliminar y consultar
enlaces. Depende de un usuario autenticado.

Autor: Henry Jiménez
Fecha: 2025-06-19
"""

from fastapi import APIRouter, Depends, status
from app.interfaces.http.api.v1.dependences import get_link_service
from app.application.dtos import LinkCreate, LinkUpdate, LinkRead
from app.application.services import LinkService


router = APIRouter(prefix="/links", tags=["links"])


@router.post("/", response_model=LinkRead, status_code=status.HTTP_201_CREATED)
def create_link(link: LinkCreate, user_id: str, link_service: LinkService = Depends(get_link_service)):
    """ Endpoint para crear un nuevo enlace. """    
    return link_service.create_link(link, user_id)

@router.get("/", response_model=list[LinkRead])
def get_links_by_user_id(user_id: str, link_service: LinkService = Depends(get_link_service)):
    """ Endpoint para consultar todos los enlaces de un usuario. """
    return link_service.get_links_by_user_id(user_id)

@router.put("/{link_id}", response_model=LinkRead)
def update_link(link_id: int, link: LinkUpdate, user_id: str, link_service: LinkService = Depends(get_link_service)):
    """ Endpoint para actualizar un enlace existente. """
    return link_service.update_link(link_id, link, user_id)

@router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(link_id: int, user_id: str, link_service: LinkService = Depends(get_link_service)):
    """ Endpoint para eliminar un enlace. """
    link_service.delete_link(link_id, user_id)

