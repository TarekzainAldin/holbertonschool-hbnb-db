import pytest
import json
from src import create_app, db
from src.models import User

@pytest.fixture
def app():
    """
    Create and configure a new app instance for each test.
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        yield app

@pytest.fixture
def client(app):
    """
    A test client for the app.
    """
    return app.test_client()

def test_login(client):
    """
    Test user login.
    """
    # Create a test user
    password = 'test_password'
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username='test_user', email='test@example.com', password=hashed_password)
    db.session.add(user)
    db.session.commit()

    # Attempt to log in with correct credentials
    response = client.post('/login', json={'email': 'test@example.com', 'password': 'test_password'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'access_token' in data

    # Attempt to log in with incorrect password
    response = client.post('/login', json={'email': 'test@example.com', 'password': 'wrong_password'})
    assert response.status_code == 401

    # Attempt to log in with non-existent user
    response = client.post('/login', json={'email': 'nonexistent@example.com', 'password': 'test_password'})
    assert response.status_code == 401
