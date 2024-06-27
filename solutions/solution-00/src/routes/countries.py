"""
This module contains the routes for the countries endpoint
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.controllers.countries import (
    create_country,
    delete_country,
    get_country_by_id,
    get_countries,
    update_country,
)
from models.user import User

countries_bp = Blueprint("countries", __name__, url_prefix="/countries")

# Public routes
countries_bp.route("/", methods=["GET"])(get_countries)
countries_bp.route("/<country_id>", methods=["GET"])(get_country_by_id)

# Routes requiring authentication and admin check
@countries_bp.route("/", methods=["POST"])
@jwt_required()
def create_country_route():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    return create_country()

@countries_bp.route("/<country_id>", methods=["PUT"])
@jwt_required()
def update_country_route(country_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    return update_country(country_id)

@countries_bp.route("/<country_id>", methods=["DELETE"])
@jwt_required()
def delete_country_route(country_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    return delete_country(country_id)
