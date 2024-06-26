import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from src import create_app, db
from src.models import User
import sys 

# Adjust the path to include the src directory where __init__.py is located
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Fixture for creating an app instance with SQLite database
@pytest.fixture(scope="module")
def app_sqlite():
    """
    Create and configure a new app instance with SQLite database for testing.
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use SQLite in memory for testing
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()  # Create all tables

    yield app

# Fixture for creating an app instance with PostgreSQL database
@pytest.fixture(scope="module")
def app_postgresql():
    """
    Create and configure a new app instance with PostgreSQL database for testing.
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['FLASK_ENV'] = 'production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/hbnb_prod'  # Adjust with your production DB URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()  # Create all tables

    yield app

# Fixture for SQLite database session
@pytest.fixture(scope="module")
def session_sqlite(app_sqlite):
    """
    Provides a SQLite database session for testing.
    """
    with app_sqlite.app_context():
        yield db.session

# Fixture for PostgreSQL database session
@pytest.fixture(scope="module")
def session_postgresql(app_postgresql):
    """
    Provides a PostgreSQL database session for testing.
    """
    with app_postgresql.app_context():
        yield db.session

# Test to verify database connection based on environment (SQLite)
def test_sqlite_database_connection(session_sqlite):
    """
    Test SQLite database connection and basic CRUD operations.
    """
    # Create a user
    new_user = User(username='test_user_sqlite', email='test_sqlite@example.com')
    session_sqlite.add(new_user)
    session_sqlite.commit()

    # Retrieve the user
    retrieved_user = session_sqlite.query(User).filter_by(username='test_user_sqlite').first()
    assert retrieved_user is not None

    # Update the user
    retrieved_user.email = 'updated_sqlite@example.com'
    session_sqlite.commit()

    # Verify the update
    updated_user = session_sqlite.query(User).filter_by(username='test_user_sqlite').first()
    assert updated_user.email == 'updated_sqlite@example.com'

    # Delete the user
    session_sqlite.delete(updated_user)
    session_sqlite.commit()

    # Ensure deletion
    deleted_user = session_sqlite.query(User).filter_by(username='test_user_sqlite').first()
    assert deleted_user is None

# Test to verify database connection based on environment (PostgreSQL)
def test_postgresql_database_connection(session_postgresql):
    """
    Test PostgreSQL database connection and basic CRUD operations.
    """
    # Create a user
    new_user = User(username='test_user_postgresql', email='test_postgresql@example.com')
    session_postgresql.add(new_user)
    session_postgresql.commit()

    # Retrieve the user
    retrieved_user = session_postgresql.query(User).filter_by(username='test_user_postgresql').first()
    assert retrieved_user is not None

    # Update the user
    retrieved_user.email = 'updated_postgresql@example.com'
    session_postgresql.commit()

    # Verify the update
    updated_user = session_postgresql.query(User).filter_by(username='test_user_postgresql').first()
    assert updated_user.email == 'updated_postgresql@example.com'

    # Delete the user
    session_postgresql.delete(updated_user)
    session_postgresql.commit()

    # Ensure deletion
    deleted_user = session_postgresql.query(User).filter_by(username='test_user_postgresql').first()
    assert deleted_user is None

# Test to ensure seamless transition between SQLite and PostgreSQL databases
def test_database_transition(session_sqlite, session_postgresql):
    """
    Test transition between SQLite and PostgreSQL databases without changes in business logic.
    """
    # Create a user in SQLite
    new_user_sqlite = User(username='test_user_transition', email='test_transition@example.com')
    session_sqlite.add(new_user_sqlite)
    session_sqlite.commit()

    # Retrieve the user from SQLite
    retrieved_user_sqlite = session_sqlite.query(User).filter_by(username='test_user_transition').first()
    assert retrieved_user_sqlite is not None

    # Move user to PostgreSQL
    try:
        session_postgresql.add(retrieved_user_sqlite)
        session_postgresql.commit()
    except SQLAlchemyError as e:
        session_postgresql.rollback()
        pytest.fail(f"Failed to transition user from SQLite to PostgreSQL: {str(e)}")

    # Retrieve the user from PostgreSQL
    retrieved_user_postgresql = session_postgresql.query(User).filter_by(username='test_user_transition').first()
    assert retrieved_user_postgresql is not None

    # Update user in PostgreSQL
    retrieved_user_postgresql.email = 'updated_transition@example.com'
    session_postgresql.commit()

    # Verify the update
    updated_user_postgresql = session_postgresql.query(User).filter_by(username='test_user_transition').first()
    assert updated_user_postgresql.email == 'updated_transition@example.com'

    # Delete user from PostgreSQL
    session_postgresql.delete(updated_user_postgresql)
    session_postgresql.commit()

    # Ensure deletion
    deleted_user_postgresql = session_postgresql.query(User).filter_by(username='test_user_transition').first()
    assert deleted_user_postgresql is None
