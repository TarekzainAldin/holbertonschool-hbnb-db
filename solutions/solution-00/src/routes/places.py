"""
This module contains the routes for the places blueprint
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.controllers.places import (
    create_place,
    delete_place,
    get_place_by_id,
    get_places,
    update_place,
)
from models.user import User

places_bp = Blueprint("places", __name__, url_prefix="/places")

# Public routes
places_bp.route("/", methods=["GET"])(get_places)
places_bp.route("/<place_id>", methods=["GET"])(get_place_by_id)

# Routes requiring authentication and admin check
@places_bp.route("/", methods=["POST"])
@jwt_required()
def create_place_route():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    return create_place()

@places_bp.route("/<place_id>", methods=["PUT"])
@jwt_required()
def update_place_route(place_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    return update_place(place_id)

@places_bp.route("/<place_id>", methods=["DELETE"])
@jwt_required()
def delete_place_route(place_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    return delete_place(place_id)
