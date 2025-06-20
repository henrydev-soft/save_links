"""
Implementación de repositorio de enlaces utilizando Firebase

Autor: Henry Jiménez
Fecha: 2025-06-18
"""

from app.domain.models import Link, NewLink
from app.domain.repositories import ILinkRepository
from app.infrastructure.firebase import firebase_client
from typing import List
from datetime import datetime, timezone
from uuid import uuid4


class FirebaseLinkRepository(ILinkRepository):
    
    def get_links_by_user_id(self, user_id: str) -> List[Link]:
        """ Obtiene todos los enlaces asociados a un usuario. """
        links = firebase_client.collection("links").where("user_id", "==", user_id).get()
        return [Link(
            id=link.id,
            url=link.get("url"),
            title=link.get("title"),
            description=link.get("description"),
            created_at=link.get("created_at"),
            user_id=link.get("user_id"),
            tags=link.get("tags")
        ) for link in links]
    
    def get_link_by_id(self, link_id) -> Link:
        """ Obtiene un enlace por su identificador. """
        link = firebase_client.collection("links").document(link_id).get() 
        if not link: 
            return None      
        return Link(
            id=link.id,
            url=link.get("url"),
            title=link.get("title"),
            description=link.get("description"),
            created_at=link.get("created_at"),
            user_id=link.get("user_id"),
            tags=link.get("tags")
        )
    
    def create_link(self, link: NewLink)-> Link:
        """ Crea un nuevo enlace en el repositorio. """
        
        #Generar ID para el nuevo Enlace
        link_id = str(uuid4())
        
        #Fecha de creación
        created_at = datetime.now(timezone.utc)
        
        link_dict = {
            "id":link_id,
            "url":link.url,
            "title":link.title,
            "description":link.description,
            "created_at":created_at,
            "tags":link.tags,
            "user_id":link.user_id
        }
        
        firebase_client.collection("links").document(link_id).set(link_dict)
        
        create_link = Link(
            id=link_id,
            url=link.url,
            title=link.title,
            description=link.description,
            created_at=created_at,
            user_id=link.user_id,
            tags=link.tags
        )
        
        
        return create_link
    
    def update_link(self, link: Link) -> Link:
        """Actualiza un enlace existente. Se asume que su existencia ya fue validada en la capa de servicio."""
        update_data = {
            "url": link.url,
            "title": link.title,
            "description": link.description,
            "tags": link.tags
        }

        firebase_client.collection("links").document(link.id).update(update_data)
        return link

    def delete_link(self, link_id: str) -> None:
        """ Elimina un enlace por su identificador. Se asume que su existencia ya fue validada en la capa de servicio."""
        firebase_client.collection("links").document(link_id).delete()
