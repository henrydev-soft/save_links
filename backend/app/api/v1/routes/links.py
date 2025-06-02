"""
Endpoints para manejar enlaces (links) en la aplicación FastAPI.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas import links as links_schema
from app.crud import links as links_crud

router = APIRouter()

@router.post("/", response_model=links_schema.Link, status_code=status.HTTP_201_CREATED)
def create_link(link: links_schema.LinkCreate, db: Session = Depends(get_db)):
    """
    Endpoint para crear un nuevo enlace.
    Utiliza la sesión de base de datos proporcionada por la dependencia `get_db`.
    """
    db_link = links_crud.get_link_by_url(db, url=link.url)
    if db_link:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Link already exists")
    else:
        db_link = links_crud.create_link(db=db, link=link)
        if not db_link:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating link")
        return db_link



@router.get("/", response_model=List[links_schema.Link])
def read_links(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Endpoint para obtener una lista de enlaces.
    Utiliza la sesión de base de datos proporcionada por la dependencia `get_db`.
    """
    links = links_crud.get_links(db, skip=skip, limit=limit)
    return links

@router.get("/{link_id}", response_model=links_schema.Link)
def read_link(link_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para obtener un enlace por su ID.
    Utiliza la sesión de base de datos proporcionada por la dependencia `get_db`.
    """
    db_link = links_crud.get_link(db, link_id=link_id)
    if not db_link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    return db_link

@router.put("/{link_id}", response_model=links_schema.Link)
def update_link(link_id: int, link: links_schema.LinkUpdate, db: Session = Depends(get_db)):
    """
    Endpoint para actualizar un enlace existente.
    Utiliza la sesión de base de datos proporcionada por la dependencia `get_db`.
    """
    db_link = links_crud.update_link(db, link_id=link_id, link=link)
    if not db_link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    return db_link

@router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(link_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para eliminar un enlace por su ID.
    Utiliza la sesión de base de datos proporcionada por la dependencia `get_db`.
    """
    db_link = links_crud.delete_link(db, link_id=link_id)
    if not db_link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    return db_link