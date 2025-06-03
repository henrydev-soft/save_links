"""
Endpoints para manejar enlaces (links) en la aplicación FastAPI.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas import links as links_schema
from app.crud import links as links_crud
from app.api.v1.deps import get_current_user_uid


router = APIRouter()

@router.post("/", response_model=links_schema.Link, status_code=status.HTTP_201_CREATED)
def create_link(
    link: links_schema.LinkCreate, 
    db: Session = Depends(get_db), 
    current_user_uid: str = Depends(get_current_user_uid)
):
    """
    Endpoint para crear un nuevo enlace.
    Utiliza la sesión de base de datos proporcionada por la dependencia `get_db`.
    """
    db_link = links_crud.get_link_by_url_and_owner(db, url=link.url,  owner_uid=current_user_uid)
    if db_link:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Link already exists")
    else:
        db_link = links_crud.create_link(db=db, link=link,  owner_uid=current_user_uid)
        if not db_link:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating link")
        return db_link



@router.get("/", response_model=List[links_schema.Link])
def read_links(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user_uid: str = Depends(get_current_user_uid)
):
    """
    Endpoint para obtener una lista de enlaces.
    Utiliza la sesión de base de datos proporcionada por la dependencia `get_db`.
    """
    links = links_crud.get_links_by_owner(db, owner_uid=current_user_uid, skip=skip, limit=limit)
    return links

@router.get("/{link_id}", response_model=links_schema.Link)
def read_link(
    link_id: int, 
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_current_user_uid)
):
    """
    Endpoint para obtener un enlace por su ID.
    Utiliza la sesión de base de datos proporcionada por la dependencia `get_db`.
    """
    db_link = links_crud.get_link_by_id_and_owner(db, link_id=link_id, owner_uid=current_user_uid)
    if not db_link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    return db_link

@router.put("/{link_id}", response_model=links_schema.Link)
def update_link(
    link_id: int, 
    link: links_schema.LinkUpdate, 
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_current_user_uid)
):
    """
    Endpoint para actualizar un enlace existente.
    Utiliza la sesión de base de datos proporcionada por la dependencia `get_db`.
    """
    db_link = links_crud.get_link_by_id_and_owner(db, link_id=link_id, owner_uid=current_user_uid)
    if db_link is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link no encontrado.")
    
    #Si el usuario intenta cambiar la URL y ya tiene esa URL guardada, se bloquea
    if link.url and link.url != db_link.url:
        existing_link_for_user = links_crud.get_link_by_url_and_owner(db, url=link.url, owner_uid=current_user_uid)
        if existing_link_for_user and existing_link_for_user.id != link_id: # Asegurarse de que no sea el mismo link
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya tienes otro link con esta URL."
            )

    return links_crud.update_link(db=db, link_id=link_id, link=link)

@router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(
    link_id: int, 
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_current_user_uid)
):
    """
    Endpoint para eliminar un enlace por su ID.
    Utiliza la sesión de base de datos proporcionada por la dependencia `get_db`.
    """
    # Verificar si el enlace existe y pertenece al usuario actual
    db_link = links_crud.get_link_by_id_and_owner(db, link_id=link_id, owner_uid=current_user_uid)
    if db_link is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link no encontrado.")

    # Eliminar el enlace
    db_link = links_crud.delete_link(db, link_id=link_id)
    if not db_link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error al eliminar el link.")
    return db_link