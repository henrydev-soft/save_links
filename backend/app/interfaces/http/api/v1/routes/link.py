"""
Rutas HTTP para la gestión de enlaces

Define los endpoints REST para crear, actualizar, eliminar y consultar
enlaces. Depende de un usuario autenticado.

Autor: Henry Jiménez
Fecha: 2025-06-19
"""

from fastapi import APIRouter, Depends, status
from app.interfaces.http.api.v1.dependences import get_link_service, get_current_user_uid
from app.application.dtos import LinkCreate, LinkUpdate, LinkRead
from app.application.services import LinkService


router = APIRouter(tags=["links"])


@router.post("/{user_id}/links", response_model=LinkRead, status_code=status.HTTP_201_CREATED)
def create_link(
    user_id: str,
    link: LinkCreate, 
    link_service: LinkService = Depends(get_link_service),
    user_data: dict = Depends(get_current_user_uid)
    ):
    """ Endpoint para crear un nuevo enlace. """    
    return link_service.create_link(link, user_id, user_data)

@router.get("/{user_id}/links", response_model=list[LinkRead])
def get_links_by_user_id(
    user_id: str,
    link_service: LinkService = Depends(get_link_service),
    user_data: dict = Depends(get_current_user_uid)
    ):
    """ Endpoint para consultar todos los enlaces de un usuario. """
    return link_service.get_links_by_user_id(user_id, user_data)

@router.put("/{user_id}/links/{link_id}", response_model=LinkRead)
def update_link(
    user_id: str, 
    link_id: str, 
    link: LinkUpdate, 
    link_service: LinkService = Depends(get_link_service),
    user_data: dict = Depends(get_current_user_uid)):
    """ Endpoint para actualizar un enlace existente. """
    return link_service.update_link(user_id, link_id, link, user_data)

@router.delete("/{user_id}/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(
    user_id: str,
    link_id: str,
    link_service: LinkService = Depends(get_link_service),
    user_data: dict = Depends(get_current_user_uid)):
    """ Endpoint para eliminar un enlace. """
    link_service.delete_link(user_id, link_id, user_data)