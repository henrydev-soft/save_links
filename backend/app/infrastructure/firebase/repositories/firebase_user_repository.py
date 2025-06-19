"""
Implementación de repositorio de usuarios utilizando Firebase

Autor: Henry Jiménez
Fecha: 2025-06-19
"""

from app.domain.models import User
from app.domain.repositories import IUserRepository
from app.infrastructure.firebase import firebase_client

class FirebaseUserRepository(IUserRepository):
    
    def get_user_by_id(self, user_id: str) -> User:
        """Obtiene un usuario por su identificador."""
        user_dict = firebase_client.collection("users").document(user_id).get().to_dict()
        return User(
            id=user_id,
            email=user_dict.get("email"),
            password=user_dict.get("password")
        )
        
    
    def create_user(self, user: User) -> User:
        """ Crea un nuevo usuario en el repositorio. """
        user_dict = {
            "id": user.id,
            "email": user.email, 
            "username": user.username
        }
        
        firebase_client.collection("users").document(user.id).set(user_dict)
        
        return user
    
    def update_user(self, user: User) -> User:
        """ Actualiza un usuario existente. """
        
        user_dict = {
            "id": user.id,
            "email": user.email, 
            "username": user.username
        }
        
        firebase_client.collection("users").document(user.id).set(user_dict)
        
        return user
        
    
    def delete_user(self, user_id: str) -> None:
        """ Elimina un usuario existente en el repositorio. """
        firebase_client.collection("users").document(user_id).delete()
