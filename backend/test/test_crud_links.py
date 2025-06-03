"""
Test Unitarios Para el CRUD de Links
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.db.base import Base
from app.crud import links as link_crud
from app.schemas import links as link_schemas
from app.db.models import Link

#Cofigurar una base de datos en memoria para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="function")
def db():
    """
    Fixtura para crear una sesión de base de datos para pruebas.
    Cada test correrá en su propia transacción y se hará rollback/limpieza.
    """
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
        Base.metadata.drop_all(bind=engine_test)

def test_create_link(db: Session):
    """
    Prueba para crear un enlace.
    """
    link_data = link_schemas.LinkCreate(url="http://example.com/test1", title="Example", description="An example link")
    created_link = link_crud.create_link(db=db, link=link_data, owner_uid="user_test_1")
    
    assert created_link.id is not None
    assert created_link.url == "http://example.com/test1"
    assert created_link.title == "Example"
    assert created_link.description == "An example link"
    assert created_link.owner_uid == "user_test_1"
    
def test_create_duplicate_link_different_owner(db: Session):
    """
    Prueba para crear un enlace duplicado con un propietario diferente.
    """
    link_data = link_schemas.LinkCreate(url="http://example.com/test2", title="Example", description="An example link")
    created_link = link_crud.create_link(db=db, link=link_data, owner_uid="user_test_1")
    assert created_link.id is not None
    assert created_link.url == "http://example.com/test2"
    assert created_link.owner_uid == "user_test_1"
    
    # Intentar crear el mismo enlace con un propietario diferente
    duplicate_link_data = link_schemas.LinkCreate(url="http://example.com/test2", title="Example", description="An example link")
    created_duplicate_link = link_crud.create_link(db=db, link=duplicate_link_data, owner_uid="user_test_2")
    
    assert created_duplicate_link.id is not None
    assert created_duplicate_link.url == "http://example.com/test2"
    assert created_duplicate_link.title == "Example"
    assert created_duplicate_link.description == "An example link"
    assert created_duplicate_link.owner_uid == "user_test_2"
    
    #Verificar que ambos enlaces existen
    assert link_crud.get_link_by_id_and_owner(db, created_link.id, "user_test_1") is not None
    assert link_crud.get_link_by_id_and_owner(db, created_duplicate_link.id, "user_test_2") is not None

def test_get_link_by_id_and_owner(db: Session):
    """
    Prueba para obtener un enlace por ID y owner_uid.
    """
    link_data = link_schemas.LinkCreate(url="http://example.com/get1", title="Example", description="An example link")
    created_link = link_crud.create_link(db=db, link=link_data, owner_uid="user_get_1")
    
    retrieved_link = link_crud.get_link_by_id_and_owner(db=db, link_id=created_link.id, owner_uid="user_get_1")
    
    assert retrieved_link is not None
    assert retrieved_link.id == created_link.id
    assert retrieved_link.url == "http://example.com/get1"
    assert retrieved_link.title == "Example"
    assert retrieved_link.description == "An example link"
    assert retrieved_link.owner_uid == "user_get_1"

def test_get_link_not_found(db: Session):
    """
    Prueba para obtener un enlace que no existe.
    """
    retrieved_link = link_crud.get_link_by_id_and_owner(db=db, link_id=9999, owner_uid="any_user")  # ID que no existe
    assert retrieved_link is None

def test_get_link_by_url_and_owner(db: Session):
    """
    Prueba para obtener un enlace por URL y owner_uid.
    """
    url_to_find = "http://example.com/get2"
    link_data = link_schemas.LinkCreate(url=url_to_find, title="Example", description="An example link")
    created_link = link_crud.create_link(db=db, link=link_data, owner_uid="user_get_2")
    
    # Crear un link con la misma URL pero diferente owner
    link_data_other_owner = link_schemas.LinkCreate(url=url_to_find, title="By URL Owner Other", description="An example link")
    created_other_owner = link_crud.create_link(db=db, link=link_data_other_owner, owner_uid="other_user_get_2")
    
    #Obtener el enlace por URL y owner_uid iniciales
    retrieved_link = link_crud.get_link_by_url_and_owner(db=db, url=url_to_find, owner_uid="user_get_2")
    assert retrieved_link is not None
    assert retrieved_link.id == created_link.id
    assert retrieved_link.url == url_to_find
    assert retrieved_link.title == "Example"
    assert retrieved_link.description == "An example link"
    assert retrieved_link.owner_uid == "user_get_2"
    
    # Intentar obtener el enlace con un owner_uid que tiene el mismo URL pero diferente owner
    retrieved_link_other_owner = link_crud.get_link_by_url_and_owner(db=db, url=url_to_find, owner_uid="other_user_get_2")
    assert retrieved_link_other_owner is not None
    assert retrieved_link_other_owner.id == created_other_owner.id
    assert retrieved_link_other_owner.url == url_to_find
    assert retrieved_link_other_owner.owner_uid == "other_user_get_2"
    
    #Intenta obtener el enlace con un owner_uid incorrecto
    retrieved_link_wrong_owner = link_crud.get_link_by_url_and_owner(db=db, url=url_to_find, owner_uid="wrong_user")
    assert retrieved_link_wrong_owner is None


def test_get_links_by_owner(db: Session):
    """
    Prueba para obtener todos los enlaces.
    """
    link_data1 = link_schemas.LinkCreate(url="http://example1.com", title="Example 1", description="An example link 1")
    link_data2 = link_schemas.LinkCreate(url="http://example2.com", title="Example 2", description="An example link 2")
    
    created_link1 = link_crud.create_link(db=db, link=link_data1, owner_uid="user_links_a")
    created_link2 = link_crud.create_link(db=db, link=link_data2, owner_uid="user_links_a")
    
    link_data3 = link_schemas.LinkCreate(url="http://example3.com", title="Example 3", description="An example link 3")
    created_link3 = link_crud.create_link(db=db, link=link_data3, owner_uid="user_links_b")
    
    #Obtener enlaces para owner "user_links_a"
    links_a = link_crud.get_links_by_owner(db=db, owner_uid="user_links_a")    
    assert len(links_a) == 2
    assert created_link1 in links_a
    assert created_link2 in links_a
    
    #Obtener enlaces para owner "user_links_b"
    links_b = link_crud.get_links_by_owner(db=db, owner_uid="user_links_b")
    assert len(links_b) == 1
    assert created_link3 in links_b
    
    #Obtener enlaces para un owner que no tiene enlaces
    links_none = link_crud.get_links_by_owner(db=db, owner_uid="user_links_none")
    assert len(links_none) == 0
    
    
def test_update_link(db: Session):
    """
    Prueba para actualizar un enlace, asegurando que se actualizan los campos correctos.
    """
    link_data = link_schemas.LinkCreate(url="http://example.com", title="Example", description="An example link")
    created_link = link_crud.create_link(db=db, link=link_data, owner_uid="user_update_1")
    
    update_data = link_schemas.LinkUpdate(url="http://example.com", title="Updated Example", description="An updated example link")
    updated_link = link_crud.update_link(db=db, link_id=created_link.id, link=update_data)
    
    assert updated_link is not None
    assert updated_link.id == created_link.id
    assert updated_link.url == "http://example.com"
    assert updated_link.title == "Updated Example"
    assert updated_link.description == "An updated example link"
    assert updated_link.owner_uid == "user_update_1"
    
def test_delete_link(db: Session):
    """
    Prueba para eliminar un enlace.
    """
    link_data = link_schemas.LinkCreate(url="http://example.com", title="Example", description="An example link")
    created_link = link_crud.create_link(db=db, link=link_data, owner_uid="user_delete_1")
    
    deleted = link_crud.delete_link(db=db, link_id=created_link.id)
    
    assert deleted is True
    assert link_crud.get_link_by_id_and_owner(db=db, link_id=created_link.id, owner_uid="user_delete_1") is None


def test_delete_link_not_found(db: Session):
    """
    Prueba para eliminar un enlace que no existe.
    """
    deleted = link_crud.delete_link(db=db, link_id=9999)  # ID que no existe
    assert deleted is False