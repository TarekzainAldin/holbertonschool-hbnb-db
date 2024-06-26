# src/__init__.py

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

# Initialize extensions
cors = CORS()
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    """
    Create a Flask app with the appropriate configuration.
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # Load configuration based on environment
    if app.env == 'production':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    elif app.env == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///hbnb_dev.db')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    cors.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    # Register routes and error handlers
    register_extensions(app)
    register_routes(app)
    register_handlers(app)

    return app

def register_extensions(app):
    """Register extensions like CORS, SQLAlchemy, and JWT"""
    cors.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

def register_routes(app):
    """Register Flask routes"""
    from src.routes import (
        users_bp, countries_bp, cities_bp, places_bp, amenities_bp, reviews_bp
    )
    app.register_blueprint(users_bp)
    app.register_blueprint(countries_bp)
    app.register_blueprint(cities_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(amenities_bp)
    app.register_blueprint(reviews_bp)

def register_handlers(app):
    """Register error handlers"""
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not found", "message": str(error)}, 404

    @app.errorhandler(400)
    def bad_request(error):
        return {"error": "Bad request", "message": str(error)}, 400

# Import JWT-related functions and decorators
from src.auth import *

# Load models to ensure they are registered with SQLAlchemy
from src.models import *

# Load routes to ensure they are registered with Flask
from src.routes import *
