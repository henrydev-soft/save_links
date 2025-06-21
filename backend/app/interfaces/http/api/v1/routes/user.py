"""
Rutas HTTP para la gestión de usuarios

Define los endpoints REST para crear, actualizar, eliminar y consultar
usuarios.

Autor: Henry Jiménez
Fecha: 2025-06-19
"""

from fastapi import APIRouter, Depends, status
from app.interfaces.http.api.v1.dependences import get_user_service, get_current_user_uid
from app.application.dtos import UserCreate, UserUpdate, UserRead
from app.application.services import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate, 
    user_service: UserService = Depends(get_user_service),
    user_data: dict = Depends(get_current_user_uid)
    ):
    """ Endpoint para crear un nuevo usuario. """
    return user_service.create_user(user, user_data)

@router.get("/{user_id}", response_model=UserRead)
def get_user_by_id(
    user_id: str, 
    user_service: UserService = Depends(get_user_service),
    user_data: dict = Depends(get_current_user_uid)):
    """ Endpoint para consultar un usuario por su id. """
    return user_service.get_user_by_id(user_id, user_data)

@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: str, 
    user: UserUpdate, 
    user_service: UserService = Depends(get_user_service),
    user_data: dict = Depends(get_current_user_uid)): 
    """ Endpoint para actualizar un usuario existente. """ 
    return user_service.update_user(user_id, user, user_data)

@router.delete("/{user_id}")
def delete_user(
    user_id: str, 
    user_service: UserService = Depends(get_user_service),
    user_data: dict = Depends(get_current_user_uid)):
    """ Endpoint para eliminar un usuario existente. """
    return user_service.delete_user(user_id, user_data)