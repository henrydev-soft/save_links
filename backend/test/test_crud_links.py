"""
Test Unitarios Para el CRUD de Links
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.db.base import Base
from app.db.session import get_db
from app.crud import links as link_crud
from app.schemas import links as link_schemas
from app.db.models import Link

#Cofigurar una base de datos en memoria para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

def override_get_db():
    """
    Función para sobreescribir la función get_db para usar una sesión de prueba.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def db():
    """
    Fixture para crear una sesión de base de datos para pruebas.
    """
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        Base.metadata.drop_all(bind=engine_test)

def test_create_link(db: Session):
    """
    Prueba para crear un enlace.
    """
    link_data = link_schemas.LinkCreate(url="http://example.com", title="Example", description="An example link")
    created_link = link_crud.create_link(db=db, link=link_data)
    
    assert created_link.id is not None
    assert created_link.url == "http://example.com"
    assert created_link.title == "Example"
    assert created_link.description == "An example link"

def test_get_link(db: Session):
    """
    Prueba para obtener un enlace por ID.
    """
    link_data = link_schemas.LinkCreate(url="http://example.com", title="Example", description="An example link")
    created_link = link_crud.create_link(db=db, link=link_data)
    
    retrieved_link = link_crud.get_link(db=db, link_id=created_link.id)
    
    assert retrieved_link is not None
    assert retrieved_link.id == created_link.id
    assert retrieved_link.url == "http://example.com"
    assert retrieved_link.title == "Example"
    assert retrieved_link.description == "An example link"

def test_get_link_not_found(db: Session):
    """
    Prueba para obtener un enlace que no existe.
    """
    retrieved_link = link_crud.get_link(db=db, link_id=9999)  # ID que no existe
    assert retrieved_link is None

def test_get_link_by_url(db: Session):
    """
    Prueba para obtener un enlace por URL.
    """
    link_data = link_schemas.LinkCreate(url="http://example.com", title="Example", description="An example link")
    created_link = link_crud.create_link(db=db, link=link_data)
    
    retrieved_link = link_crud.get_link_by_url(db=db, url="http://example.com")
    
    assert retrieved_link is not None
    assert retrieved_link.id == created_link.id
    assert retrieved_link.url == "http://example.com"
    assert retrieved_link.title == "Example"
    assert retrieved_link.description == "An example link"


def test_get_links(db: Session):
    """
    Prueba para obtener todos los enlaces.
    """
    link_data1 = link_schemas.LinkCreate(url="http://example1.com", title="Example 1", description="An example link 1")
    link_data2 = link_schemas.LinkCreate(url="http://example2.com", title="Example 2", description="An example link 2")
    
    created_link1 = link_crud.create_link(db=db, link=link_data1)
    created_link2 = link_crud.create_link(db=db, link=link_data2)
    
    links = link_crud.get_links(db=db)
    
    assert len(links) == 2
    assert created_link1 in links
    assert created_link2 in links
    
def test_update_link(db: Session):
    """
    Prueba para actualizar un enlace.
    """
    link_data = link_schemas.LinkCreate(url="http://example.com", title="Example", description="An example link")
    created_link = link_crud.create_link(db=db, link=link_data)
    
    update_data = link_schemas.LinkUpdate(url="http://example.com", title="Updated Example", description="An updated example link")
    updated_link = link_crud.update_link(db=db, link_id=created_link.id, link=update_data)
    
    assert updated_link is not None
    assert updated_link.id == created_link.id
    assert updated_link.url == "http://example.com"
    assert updated_link.title == "Updated Example"
    assert updated_link.description == "An updated example link"
    
def test_delete_link(db: Session):
    """
    Prueba para eliminar un enlace.
    """
    link_data = link_schemas.LinkCreate(url="http://example.com", title="Example", description="An example link")
    created_link = link_crud.create_link(db=db, link=link_data)
    
    deleted = link_crud.delete_link(db=db, link_id=created_link.id)
    
    assert deleted is True
    assert link_crud.get_link(db=db, link_id=created_link.id) is None
    
    # Verificar que el enlace ya no existe
    retrieved_link = link_crud.get_link(db=db, link_id=created_link.id)
    assert retrieved_link is None


def test_delete_link_not_found(db: Session):
    """
    Prueba para eliminar un enlace que no existe.
    """
    deleted = link_crud.delete_link(db=db, link_id=9999)  # ID que no existe
    assert deleted is False