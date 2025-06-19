"""
Este archivo encapsula la construcción de servicios de aplicación,
inyectando los repositorios adecuados desde la capa de infraestructura.

Facilita el uso de FastAPI.Depends sin acoplar los routers a Firebase.

Autor: Henry Jimenez
Fecha: 2025-06-11
"""
from functools import lru_cache
from app.application.services import UserService, LinkService
from app.infrastructure.firebase.repositories import FirebaseUserRepository, FirebaseLinkRepository


@lru_cache
def get_user_service() -> UserService:
    """ Obtiene una instancia del servicio de usuarios. """
    
    # TODO: Inyectar dependencias
    user_repository = FirebaseUserRepository()
    
    return UserService(user_repository)

@lru_cache
def get_link_service() -> LinkService:
    """ Obtiene una instancia del servicio de enlaces. """
    
    # TODO: Inyectar dependencias
    user_repository = FirebaseUserRepository()
    link_repository = FirebaseLinkRepository()
    
    return LinkService(link_repository, user_repository)