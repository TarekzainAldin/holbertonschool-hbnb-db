from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.config import get_config

app_config = get_config()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(app_config)
    db.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
