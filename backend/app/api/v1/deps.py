"""
Archivo de dependencias para la autenticación y autorización de usuarios en FastAPI.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from firebase_admin import auth
from firebase_admin.auth import InvalidIdTokenError, ExpiredIdTokenError

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
    try:
        # Verifica el token usando el SDK de Firebase Admin
        # Si el token es válido, devuelve un diccionario con los datos decodificados.
        decoded_token = auth.verify_id_token(token)
        # Extrae el User ID (UID) del token decodificado
        uid = decoded_token['uid']
        return uid
    except ExpiredIdTokenError:
        # Maneja tokens expirados
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación de Firebase ha expirado. Por favor, inicie sesión de nuevo.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidIdTokenError:
        # Maneja tokens inválidos (firmas incorrectas, etc.)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación de Firebase inválido. Acceso denegado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        # Captura cualquier otra excepción inesperada durante la verificación
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"No se pudo validar el token de Firebase: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )