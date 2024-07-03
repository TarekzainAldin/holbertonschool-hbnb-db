""" Another way to run the app"""

from src import create_app
from flask import Flask
from flask_jwt_extended import JWTManager
from src.models import db, bcrypt
from src.controllers import users

app = Flask(__name__)

# Configuration de l'application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

# Initialisation des extensions
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# Routes de votre application
app.add_url_rule('/users', 'get_users', users.get_users, methods=['GET'])
app.add_url_rule('/users', 'create_user', users.create_user, methods=['POST'])
app.add_url_rule('/users/<user_id>', 'get_user_by_id', users.get_user_by_id, methods=['GET'])
app.add_url_rule('/users/<user_id>', 'update_user', users.update_user, methods=['PUT'])
app.add_url_rule('/users/<user_id>', 'delete_user', users.delete_user, methods=['DELETE'])

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
