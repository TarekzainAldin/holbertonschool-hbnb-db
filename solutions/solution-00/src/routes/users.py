"""
This module contains the routes for the users endpoints.
"""

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.controllers.users import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
)
from src import db
from models.user import User

users_bp = Blueprint("users", __name__, url_prefix="/users")

# Routes requiring authentication
@users_bp.route("/", methods=["GET"])
@jwt_required()
def get_users_route():
    return get_users()

@users_bp.route("/", methods=["POST"])
@jwt_required()
def create_user_route():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    return create_user()

@users_bp.route("/<user_id>", methods=["GET"])
@jwt_required()
def get_user_by_id_route(user_id):
    return get_user_by_id(user_id)

@users_bp.route("/<user_id>", methods=["PUT"])
@jwt_required()
def update_user_route(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin and current_user.id != user_id:
        return jsonify({"message": "Admin access required or own account"}), 403
    return update_user(user_id)

@users_bp.route("/<user_id>", methods=["DELETE"])
@jwt_required()
def delete_user_route(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    return delete_user(user_id)

# Register route
@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(
        email=data['email'],
        password=hashed_password,
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', '')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Login route
@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

# Protected route example
@users_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    }), 200
