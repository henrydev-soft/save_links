"""
Pruebas para las rutas de la API relacionadas con los enlaces (links).
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db



# Crear base de datos temporal en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test/test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas en la base de datos de prueba
Base.metadata.create_all(bind=engine)



# Sobrescribir la dependencia get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def test_client():
    yield client

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    # Crear las tablas al inicio
    Base.metadata.create_all(bind=engine)
    yield
    # Eliminar las tablas al final
    Base.metadata.drop_all(bind=engine)


def test_create_link():
    """
    Prueba para crear un enlace a través de la API.
    """
    link_data = {
        "url": "http://examplecreate.com",
        "title": "Example",
        "description": "An example link"
    }
    response = client.post("/api/v1/links/", json=link_data)
    print(f"Respuesta de la API: {response.status_code} - {response.text}")

    assert response.status_code == 201
    created_link = response.json()
    assert created_link["id"] is not None
    assert created_link["url"] == "http://examplecreate.com"
    assert created_link["title"] == "Example"
    assert created_link["description"] == "An example link"

def test_create_link_already_exists():
    """
    Prueba para intentar crear un enlace que ya existe.
    """
    link_data = {
        "url": "http://exampleExists.com",
        "title": "Example",
        "description": "An example link"
    }
    response = client.post("/api/v1/links/", json=link_data)
    assert response.status_code == 201  # Debe crearse correctamente

    # Intentar crear el mismo enlace de nuevo
    response = client.post("/api/v1/links/", json=link_data)

    assert response.status_code == 400  # Debe fallar con un error de enlace ya existente

def test_get_link():
    """
    Prueba para obtener un enlace por ID a través de la API.
    """
    link_data = {
        "url": "http://test.com",
        "title": "Example",
        "description": "An example link"
    }
    response = client.post("/api/v1/links/", json=link_data)
    created_link = response.json()
    print(f"Enlace creado: {created_link}")
    
    response = client.get(f"/api/v1/links/{created_link['id']}")
    
    assert response.status_code == 200
    retrieved_link = response.json()
    assert retrieved_link["id"] == created_link["id"]
    assert retrieved_link["url"] == "http://test.com"
    assert retrieved_link["title"] == "Example"
    assert retrieved_link["description"] == "An example link"

def test_get_link_not_found():
    """
    Prueba para obtener un enlace que no existe.
    """
    response = client.get("/api/v1/links/9999")  # ID que no existe
    assert response.status_code == 404  # Debe devolver un error 404
    assert response.json() == {"detail": "Link not found"}

def test_get_links():
    """
    Prueba para obtener todos los enlaces a través de la API.
    """
    link_data1 = {
        "url": "http://example1.com",
        "title": "Example 1",
        "description": "An example link 1"
    }
    link_data2 = {
        "url": "http://example2.com",
        "title": "Example 2",
        "description": "An example link 2"
    }
    
    client.post("/api/v1/links/", json=link_data1)
    client.post("/api/v1/links/", json=link_data2)
    
    response = client.get("/api/v1/links/")
    
    assert response.status_code == 200
    links = response.json()
    assert len(links) >= 2  # Debe haber al menos dos enlaces
    assert any(link["url"] == "http://example1.com" for link in links)
    assert any(link["url"] == "http://example2.com" for link in links)

def test_update_link():
    """
    Prueba para actualizar un enlace a través de la API.
    """
    link_data = {
        "url": "http://update.com",
        "title": "Example",
        "description": "An example link"
    }
    response = client.post("/api/v1/links/", json=link_data)
    created_link = response.json()
    
    update_data = {
        "url": "http://updated-example.com",
        "title": "Updated Example",
        "description": "An updated example link"
    }
    
    response = client.put(f"/api/v1/links/{created_link['id']}", json=update_data)
    
    assert response.status_code == 200
    updated_link = response.json()
    assert updated_link["id"] == created_link["id"]
    assert updated_link["url"] == "http://updated-example.com"
    assert updated_link["title"] == "Updated Example"
    assert updated_link["description"] == "An updated example link"


def test_delete_link():
    """
    Prueba para eliminar un enlace a través de la API.
    """
    link_data = {
        "url": "http://delete.com",
        "title": "Example",
        "description": "An example link"
    }
    response = client.post("/api/v1/links/", json=link_data)
    created_link = response.json()
    
    response = client.delete(f"/api/v1/links/{created_link['id']}")
    
    assert response.status_code == 204  # Debe devolver un estado 204 No Content
    
    # Verificar que el enlace ya no existe
    response = client.get(f"/api/v1/links/{created_link['id']}")
    assert response.status_code == 404  # Debe devolver un error 404