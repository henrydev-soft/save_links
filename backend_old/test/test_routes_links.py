"""
Pruebas para las rutas de la API relacionadas con los enlaces (links).
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from unittest.mock import patch

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.db.models import Link



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

@pytest.fixture(scope="function", autouse=True)
def clean_db_for_each_test():
    """
    Limpia la base de datos antes de cada función de prueba.
    Esto asegura que cada test sea independiente.
    """
    with TestingSessionLocal() as session:
        # Eliminar todos los datos de la tabla 'links'
        session.query(Link).delete()
        session.commit()
    yield

# --- Fixture para mockear la autenticación de Firebase ---
@pytest.fixture
def mock_firebase_auth():
    """
    Mocks firebase_admin.auth.verify_id_token para simular autenticación.
    Por defecto, autentica como 'test_current_user_uid'.
    """
    with patch('firebase_admin.auth.verify_id_token') as mock_verify:
        mock_verify.return_value = {'uid': 'test_current_user_uid'}
        yield mock_verify

# --- Helper para obtener headers de autenticación ---
def get_auth_headers(uid: str = "test_current_user_uid"):
    """
    Retorna los headers de autorización para un UID dado.
    (El UID real es mockeado por mock_firebase_auth).
    """
    return {"Authorization": f"Bearer fake-token-for-{uid}"}

def test_create_link_authenticated(mock_firebase_auth):
    """
    Prueba para crear un enlace a través de la API, con un usuario autenticado.
    """
    link_data = {
        "url": "http://examplecreate.com",
        "title": "Example",
        "description": "An example link"
    }
    response = client.post("/api/v1/links/", json=link_data, headers=get_auth_headers())
    print(f"Respuesta de la API: {response.status_code} - {response.text}")

    assert response.status_code == 201
    created_link = response.json()
    assert created_link["id"] is not None
    assert created_link["url"] == "http://examplecreate.com"
    assert created_link["title"] == "Example"
    assert created_link["description"] == "An example link"
    assert created_link["owner_uid"] == "test_current_user_uid"

def test_create_link_unauthenticated():
    """
    Prueba para intentar crear un enlace sin autenticación.
    """
    link_data = {
        "url": "http://example.com",
        "title": "Example",
        "description": "An example link"
    }
    response = client.post("/api/v1/links/", json=link_data)

    assert response.status_code == 401  # Debe devolver un error de no autorizado
    assert response.json() == {"detail": "Not authenticated"}

def test_create_link_already_exists(mock_firebase_auth):
    """
    Prueba que el mismo usuario NO puede crear dos enlaces con la misma URL.
    """
    link_data = {
        "url": "http://exampleExists.com",
        "title": "Example",
        "description": "An example link"
    }
    response = client.post("/api/v1/links/", json=link_data,headers=get_auth_headers())
    assert response.status_code == 201  # Debe crearse correctamente

    # Intentar crear el mismo enlace de nuevo
    response = client.post("/api/v1/links/", json=link_data,headers=get_auth_headers())

    assert response.status_code == 400  # Debe fallar con un error de enlace ya existente

def test_create_duplicate_link_different_user(mock_firebase_auth):
    """
    Prueba que diferentes usuarios SÍ pueden crear enlaces con la misma URL.
    """
    test_url = "http://example.com/duplicate-different-user"
    
    # Usuario A crea el link
    mock_firebase_auth.return_value = {'uid': 'user_A'}
    link_data_a = {"url": test_url, "title": "Link by User A"}
    response_a = client.post("/api/v1/links/", json=link_data_a, headers=get_auth_headers(uid='user_A'))
    assert response_a.status_code == 201
    
    # Usuario B crea el mismo link
    mock_firebase_auth.return_value = {'uid': 'user_B'}
    link_data_b = {"url": test_url, "title": "Link by User B"}
    response_b = client.post("/api/v1/links/", json=link_data_b, headers=get_auth_headers(uid='user_B'))
    assert response_b.status_code == 201

    assert response_a.json()["id"] != response_b.json()["id"] # Deben ser IDs diferentes
    assert response_a.json()["owner_uid"] == "user_A"
    assert response_b.json()["owner_uid"] == "user_B"

def test_get_specific_link_owned(mock_firebase_auth):
    """
    Prueba para obtener un link específico que pertenece al usuario autenticado.
    """
    link_data = {
        "url": "http://test.com/get3",
        "title": "Example",
        "description": "An example link"
    }
    response = client.post("/api/v1/links/", json=link_data, headers=get_auth_headers())
    created_link = response.json()
    print(f"Enlace creado: {created_link}")
    
    response = client.get(f"/api/v1/links/{created_link['id']}", headers=get_auth_headers())
    
    assert response.status_code == 200
    retrieved_link = response.json()
    assert retrieved_link["id"] == created_link["id"]
    assert retrieved_link["url"] == "http://test.com/get3"
    assert retrieved_link["title"] == "Example"
    assert retrieved_link["description"] == "An example link"
    assert retrieved_link["owner_uid"] == "test_current_user_uid"


def get_specific_link_not_owned(mock_firebase_auth):
    """
    Prueba para obtener un enlace específico que NO pertenece al usuario autenticado.
    """
    link_data = {
        "url": "http://test.com/get4",
        "title": "Example",
        "description": "An example link"
    }
    response = client.post("/api/v1/links/", json=link_data, headers=get_auth_headers())
    created_link = response.json()
    
    # Cambiar el UID del mock para simular otro usuario
    mock_firebase_auth.return_value = {'uid': 'another_user'}
    
    response = client.get(f"/api/v1/links/{created_link['id']}", headers=get_auth_headers(uid='another_user'))    
    assert response.status_code == 404  # Debe devolver un error 404
    assert response.json() == {"detail": "Link not found"}

def test_get_link_not_found(mock_firebase_auth):
    """
    Prueba para obtener un enlace que no existe.
    """
    response = client.get("/api/v1/links/9999", headers=get_auth_headers())  # ID que no existe
    assert response.status_code == 404  # Debe devolver un error 404
    assert response.json() == {"detail": "Link not found"}

def test_get_links_only_owned(mock_firebase_auth):
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
    
    link_data3 = {
        "url": "http://example3.com",
        "title": "Example 3",
        "description": "An example link 3"
    }
    
    #Crear enlaces con el usuario a
    mock_firebase_auth.return_value = {'uid': 'user_A'}
    client.post("/api/v1/links/", json=link_data1, headers=get_auth_headers(uid='user_A'))
    client.post("/api/v1/links/", json=link_data2, headers=get_auth_headers(uid='user_A'))
    
    #Crear enlace con el usuario b
    mock_firebase_auth.return_value = {'uid': 'user_B'}
    client.post("/api/v1/links/", json=link_data3, headers=get_auth_headers(uid='user_B'))
    
    # Obtener enlaces del usuario A
    mock_firebase_auth.return_value = {'uid': 'user_A'}
    response = client.get("/api/v1/links/",  headers=get_auth_headers(uid='user_A'))    
    assert response.status_code == 200
    links = response.json()
    assert len(links) >= 2  # Debe haber dos enlaces del usuario A
    assert any(link["url"] == "http://example1.com" for link in links)
    assert any(link["url"] == "http://example2.com" for link in links)
    
    # Obtener enlaces del usuario B
    mock_firebase_auth.return_value = {'uid': 'user_B'}
    response = client.get("/api/v1/links/",  headers=get_auth_headers(uid='user_B'))
    assert response.status_code == 200
    links = response.json()
    assert len(links) == 1  # Debe haber un enlace del usuario B
    assert any(link["url"] == "http://example3.com" for link in links)

def test_update_link(mock_firebase_auth):
    """
    Prueba para actualizar un enlace a través de la API.
    """
    link_data = {
        "url": "http://update.com",
        "title": "Example",
        "description": "An example link"
    }
    response = client.post("/api/v1/links/", json=link_data, headers=get_auth_headers())
    created_link = response.json()
    
    update_data = {
        "url": "http://updated-example.com",
        "title": "Updated Example",
        "description": "An updated example link"
    }
    
    response = client.put(f"/api/v1/links/{created_link['id']}", json=update_data, headers=get_auth_headers())
    
    assert response.status_code == 200
    updated_link = response.json()
    assert updated_link["id"] == created_link["id"]
    assert updated_link["url"] == "http://updated-example.com"
    assert updated_link["title"] == "Updated Example"
    assert updated_link["description"] == "An updated example link"


def test_delete_link(mock_firebase_auth):
    """
    Prueba para eliminar un enlace a través de la API.
    """
    link_data = {
        "url": "http://delete.com",
        "title": "Example",
        "description": "An example link"
    }
    response = client.post("/api/v1/links/", json=link_data, headers=get_auth_headers())
    created_link = response.json()
    
    response = client.delete(f"/api/v1/links/{created_link['id']}", headers=get_auth_headers())
    
    assert response.status_code == 204  # Debe devolver un estado 204 No Content
    
    # Verificar que el enlace ya no existe
    response = client.get(f"/api/v1/links/{created_link['id']}", headers=get_auth_headers())
    assert response.status_code == 404  # Debe devolver un error 404

def test_delete_link_not_found(mock_firebase_auth):
    """
    Prueba para intentar eliminar un enlace que no existe.
    """
    response = client.delete("/api/v1/links/9999", headers=get_auth_headers())  # ID que no existe
    assert response.status_code == 404  # Debe devolver un error 404
    assert response.json() == {"detail": "Link no encontrado."}