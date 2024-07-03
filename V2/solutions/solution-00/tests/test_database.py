import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.models.user import User

from src import create_app, db  # Replace with your actual application setup

@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use SQLite in-memory for testing
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

@pytest.fixture(scope='module')
def postgres_test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/testdb'  # Replace with your PostgreSQL database URL
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

def test_sqlite_connection(test_client):
    response = test_client.get('/')  # Replace with an endpoint that verifies database connection or health
    assert response.status_code == 200
    assert b'SQLite' in response.data

def test_postgres_connection(postgres_test_client):
    response = postgres_test_client.get('/')  # Replace with an endpoint that verifies database connection or health
    assert response.status_code == 200
    assert b'PostgreSQL' in response.data

def test_sqlite_crud_operations(test_client):
    # Example CRUD operations for SQLite
    with test_client:
        # Insert
        db.session.add(User(username='testuser', email='test@example.com'))
        db.session.commit()

        # Retrieve
        user = User.query.filter_by(username='testuser').first()
        assert user is not None

        # Update
        user.email = 'new_email@example.com'
        db.session.commit()

        updated_user = User.query.filter_by(username='testuser').first()
        assert updated_user.email == 'new_email@example.com'

        # Delete
        db.session.delete(updated_user)
        db.session.commit()

        deleted_user = User.query.filter_by(username='testuser').first()
        assert deleted_user is None

def test_postgres_crud_operations(postgres_test_client):
    # Example CRUD operations for PostgreSQL
    with postgres_test_client:
        # Insert
        db.session.add(User(username='testuser', email='test@example.com'))
        db.session.commit()

        # Retrieve
        user = User.query.filter_by(username='testuser').first()
        assert user is not None

        # Update
        user.email = 'new_email@example.com'
        db.session.commit()

        updated_user = User.query.filter_by(username='testuser').first()
        assert updated_user.email == 'new_email@example.com'

        # Delete
        db.session.delete(updated_user)
        db.session.commit()

        deleted_user = User.query.filter_by(username='testuser').first()
        assert deleted_user is None
