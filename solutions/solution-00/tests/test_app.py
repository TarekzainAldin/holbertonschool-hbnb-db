import pytest
from src.__init__ import create_app, db
from src.models import User  # Adjust with your actual models

@pytest.fixture
def app():
    """
    Create and configure a new app instance for each test.
    """
    app = create_app()
    app.config['TESTING'] = True  # Enable testing mode
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use SQLite in memory for testing
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()  # Create all tables

    yield app

@pytest.fixture
def client(app):
    """
    A test client for the app.
    """
    return app.test_client()

def test_database_connection_development(client):
    """
    Test database connection in development mode (SQLite).
    """
    response = client.get('/')
    assert b'Success' in response.data  # Example assertion, replace with actual endpoint response

def test_database_connection_production(client):
    """
    Test database connection in production mode (PostgreSQL).
    """
    # Simulate production environment
    app = create_app()
    app.config['TESTING'] = True  # Enable testing mode
    app.config['FLASK_ENV'] = 'production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/hbnb_prod'  # Adjust with your production DB URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        response = client.get('/')
        assert b'Success' in response.data  # Example assertion, replace with actual endpoint response

def test_user_crud_operations(client):
    """
    Test basic CRUD operations for User model.
    """
    # Create a user
    new_user = User(username='test_user', email='test@example.com')
    db.session.add(new_user)
    db.session.commit()

    # Retrieve the user
    retrieved_user = User.query.filter_by(username='test_user').first()
    assert retrieved_user is not None

    # Update the user
    retrieved_user.email = 'updated@example.com'
    db.session.commit()

    # Verify the update
    updated_user = User.query.filter_by(username='test_user').first()
    assert updated_user.email == 'updated@example.com'

    # Delete the user
    db.session.delete(updated_user)
    db.session.commit()

    # Ensure deletion
    deleted_user = User.query.filter_by(username='test_user').first()
    assert deleted_user is None

