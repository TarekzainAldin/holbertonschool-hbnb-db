"""
This module contains the routes for the amenities blueprint
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.controllers.amenities import (
    create_amenity,
    delete_amenity,
    get_amenity_by_id,
    get_amenities,
    update_amenity,
)
from models.user import User

amenities_bp = Blueprint("amenities", __name__, url_prefix="/amenities")

# Public routes
amenities_bp.route("/", methods=["GET"])(get_amenities)
amenities_bp.route("/<amenity_id>", methods=["GET"])(get_amenity_by_id)

# Routes requiring authentication and admin check
@amenities_bp.route("/", methods=["POST"])
@jwt_required()
def create_amenity_route():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    return create_amenity()

@amenities_bp.route("/<amenity_id>", methods=["PUT"])
@jwt_required()
def update_amenity_route(amenity_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    return update_amenity(amenity_id)

@amenities_bp.route("/<amenity_id>", methods=["DELETE"])
@jwt_required()
def delete_amenity_route(amenity_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    return delete_amenity(amenity_id)
