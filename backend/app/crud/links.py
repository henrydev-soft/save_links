"""
Implementar funciones CRUD para el modelo Link en la base de datos utilizando SQLAlchemy.
"""

from sqlalchemy.orm import Session
from app.db.models import Link
from app.schemas.links import LinkCreate, LinkUpdate

def get_link(db: Session, link_id: int):
    """
    Obtiene un enlace por su ID.
    """
    return db.query(Link).filter(Link.id == link_id).first()

def get_link_by_url(db: Session, url: str):
    """
    Obtiene un enlace por su URL.
    """
    return db.query(Link).filter(Link.url == url).first()

def get_links(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene una lista de enlaces con paginación.
    """
    return db.query(Link).offset(skip).limit(limit).all()

def create_link(db: Session, link: LinkCreate):
    """
    Crea un nuevo enlace en la base de datos.
    """
    db_link = Link(**link.model_dump())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

def update_link(db: Session, link_id: int, link: LinkUpdate):
    """
    Actualiza un enlace existente en la base de datos.
    """
    db_link = db.query(Link).filter(Link.id == link_id).first()
    if db_link:
        for key, value in link.model_dump(exclude_unset=True).items():
            setattr(db_link, key, value)
        db.commit()
        db.refresh(db_link)
        return db_link
    return None

def delete_link(db: Session, link_id: int):
    """
    Elimina un enlace de la base de datos por su ID.
    """
    db_link = db.query(Link).filter(Link.id == link_id).first()
    if db_link:
        db.delete(db_link)
        db.commit()
        return True
    return False