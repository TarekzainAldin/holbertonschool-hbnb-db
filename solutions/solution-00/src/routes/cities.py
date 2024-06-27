"""
This module contains the routes for the cities blueprint
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.controllers.cities import (
    create_city,
    delete_city,
    get_city_by_id,
    get_cities,
    update_city,
)
from models.user import User

cities_bp = Blueprint("cities", __name__, url_prefix="/cities")

# Public routes
cities_bp.route("/", methods=["GET"])(get_cities)
cities_bp.route("/<city_id>", methods=["GET"])(get_city_by_id)

# Routes requiring authentication and admin check
@cities_bp.route("/", methods=["POST"])
@jwt_required()
def create_city_route():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    return create_city()

@cities_bp.route("/<city_id>", methods=["PUT"])
@jwt_required()
def update_city_route(city_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    return update_city(city_id)

@cities_bp.route("/<city_id>", methods=["DELETE"])
@jwt_required()
def delete_city_route(city_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    return delete_city(city_id)
