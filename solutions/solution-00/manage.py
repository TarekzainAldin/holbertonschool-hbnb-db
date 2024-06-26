# manage.py

import os
from flask import Flask
from flask.cli import FlaskGroup
from src.persistence.db import DBRepository
from utils.constants import REPOSITORY_ENV_VAR

# Load environment variables if specified
if os.path.exists('.env'):
    from dotenv import load_dotenv
    load_dotenv('.env')

# Create a function to create the Flask application
def create_app():
    app = Flask(__name__)

    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///./test.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

    # Initialize SQLAlchemy with the Flask application
    from src.models.base import Base
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        SessionLocal().close()

    # Register SQLAlchemy session for use in DBRepository
    app.db_session = SessionLocal()

    # Register repository based on environment variable
    if os.getenv(REPOSITORY_ENV_VAR) == "db":
        app.repo = DBRepository()
    else:
        # Handle other repositories if needed
        pass

    return app

# Create a FlaskGroup instance to manage commands
cli = FlaskGroup(create_app=create_app)

# Add commands to the CLI using FlaskGroup
@cli.command('routes')
def show_routes():
    """Show the routes for the app"""
    # Implement route listing logic here
    print("Routes will be listed here.")

@cli.command('run')
def run_server():
    """Run a development server"""
    app = create_app()
    app.run(debug=True)

@cli.command('shell')
def run_shell():
    """Run a shell in the app context"""
    app = create_app()
    with app.app_context():
        import IPython
        IPython.embed()

if __name__ == '__main__':
    cli()
