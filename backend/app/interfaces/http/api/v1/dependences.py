"""
Este archivo encapsula la construcción de servicios de aplicación,
inyectando los repositorios adecuados desde la capa de infraestructura.

Facilita el uso de FastAPI.Depends sin acoplar los routers a Firebase.

Autor: Henry Jimenez
Fecha: 2025-06-11
"""
from functools import lru_cache
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
from firebase_admin.auth import InvalidIdTokenError, ExpiredIdTokenError
from app.application.services import UserService, LinkService
from app.infrastructure.firebase.repositories import FirebaseUserRepository, FirebaseLinkRepository
from app.core import logger


security = HTTPBearer()


async def get_current_user_uid(token: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Dependencia que verifica un token de Firebase ID y devuelve el UID del usuario.
    Lanza una HTTPException si el token es inválido o ha expirado.
    
    Args:
        token (str): El token JWT proporcionado por el cliente.
    
    Returns:
        str: El UID del usuario autenticado.
    
    Raises:
        HTTPException: Si el token es inválido o ha expirado.
    """
    
    try:
        # Verifica el token usando el SDK de Firebase Admin
        # Si el token es válido, devuelve un diccionario con los datos decodificados.
        decoded_token = auth.verify_id_token(token.credentials)
        # Extrae el User ID (UID) del token decodificado
        uid = decoded_token['uid']
        email = decoded_token['email']
        logger.info(f"Token de Firebase validado exitosamente para UID: {uid}")
        return {"uid": uid, "email": email}
    except ExpiredIdTokenError as e:
        # Maneja tokens expirados
        logger.warning(f"Error: Token de Firebase ha expirado. Detalles: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación de Firebase ha expirado. Por favor, inicie sesión de nuevo.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidIdTokenError as e:
        # Maneja tokens inválidos (firmas incorrectas, etc.)
        logger.error(f"Error: Token de Firebase inválido. Detalles: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación de Firebase inválido. Acceso denegado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        # Captura cualquier otra excepción inesperada durante la verificación
        logger.critical(f"Error inesperado durante la validación del token de Firebase: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"No se pudo validar el token de Firebase: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )


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