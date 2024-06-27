# src/__init__.py

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()

def create_app(config_class="src.config.DevelopmentConfig") -> Flask:
    """
    Create a Flask app with the given configuration class.
    The default configuration class is DevelopmentConfig.
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    app.config.from_object(config_class)

    # Initialize extensions with the app context
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Register other parts of the application
    register_extensions(app)
    register_routes(app)
    register_handlers(app)

    return app

def register_extensions(app: Flask) -> None:
    """Register the extensions for the Flask app"""
    # No need to reinitialize db and cors here
    pass

def register_routes(app: Flask) -> None:
    """Import and register the routes for the Flask app"""
    from src.routes.users import users_bp
    from src.routes.countries import countries_bp
    from src.routes.cities import cities_bp
    from src.routes.places import places_bp
    from src.routes.amenities import amenities_bp
    from src.routes.reviews import reviews_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(countries_bp)
    app.register_blueprint(cities_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(amenities_bp)

def register_handlers(app: Flask) -> None:
    """Register the error handlers for the Flask app."""
    app.errorhandler(404)(lambda e: (
        {"error": "Not found", "message": str(e)}, 404
    ))
    app.errorhandler(400)(
        lambda e: (
            {"error": "Bad request", "message": str(e)}, 400
        )
    )

# Import db and models
from src.persistence import db
from src.models.base import Base
from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
