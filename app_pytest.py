import os
import tempfile
import pytest
from app import app, db, User, Chats, generate_unique_session_id

@pytest.fixture
def client():
    # Use an in-memory SQLite database for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_register_route(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_login_route(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_logout_route(client):
    response = client.get('/logout')
    assert response.status_code == 302  # Redirect to login page

def test_new_session_route(client):
    response = client.get('/new_session')
    assert response.status_code == 302  # Redirect to user page

def test_user_route(client):
    response = client.get('/user')
    assert response.status_code == 302  # Redirect to login page

def test_fetch_conversation_route(client):
    response = client.get('/fetch_conversation/null')
    assert response.status_code == 200
    assert response.get_json() == []

def test_fetch_sessions_Ids_route(client):
    response = client.get('/fetch_sessions_Ids')
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_data_route(client):
    response = client.post('/data', json={'data': 'test'})
    assert response.status_code == 200
    assert response.get_json()['response'] == True

def test_register_user(client):
    response = client.post('/register', data={'name': 'Test User', 'email': 'test@example.com', 'password': 'test123'})
    assert response.status_code == 200  # Redirect to login page

def test_login_user(client):
    client.post('/register', data={'name': 'Test User', 'email': 'test@example.com', 'password': 'test123'})
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'test123'})
    assert response.status_code == 200  # Redirect to user page

def test_logout_user(client):
    client.post('/register', data={'name': 'Test User', 'email': 'test@example.com', 'password': 'test123'})
    client.post('/login', data={'email': 'test@example.com', 'password': 'test123'})
    response = client.get('/logout')
    assert response.status_code == 302  # Redirect to login page

def test_fetch_conversation_for_session(client):
    client.post('/register', data={'name': 'Test User', 'email': 'test@example.com', 'password': 'test123'})
    client.post('/login', data={'email': 'test@example.com', 'password': 'test123'})
    session_id = generate_unique_session_id()
    response = client.get(f'/fetch_conversation/{session_id}')
    assert response.status_code == 200
    assert response.get_json() == []

def test_fetch_sessions_Ids_for_user(client):
    client.post('/register', data={'name': 'Test User', 'email': 'test@example.com', 'password': 'test123'})
    client.post('/login', data={'email': 'test@example.com', 'password': 'test123'})
    response = client.get('/fetch_sessions_Ids')
    assert response.status_code == 200
    assert response.get_json() == []

# Add more test cases as needed

