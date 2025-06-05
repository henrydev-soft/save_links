"""
Archivo de dependencias para la autenticación y autorización de usuarios en FastAPI.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from firebase_admin import auth
from firebase_admin.auth import InvalidIdTokenError, ExpiredIdTokenError

import logging

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user_uid(token: str = Depends(oauth2_scheme)):
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
    logger = logging.getLogger(__name__)
    
    try:
        # Verifica el token usando el SDK de Firebase Admin
        # Si el token es válido, devuelve un diccionario con los datos decodificados.
        decoded_token = auth.verify_id_token(token)
        # Extrae el User ID (UID) del token decodificado
        uid = decoded_token['uid']
        logger.info(f"Token de Firebase validado exitosamente para UID: {uid}")
        return uid
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