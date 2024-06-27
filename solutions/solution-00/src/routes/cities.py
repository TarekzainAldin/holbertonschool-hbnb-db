"""
This module contains the routes for the cities blueprint.
"""

from flask import Blueprint
from flask_jwt_extended import jwt_required
from src.decorators import admin_required  # Import the admin_required decorator
from src.controllers.cities import (
    create_city,
    delete_city,
    get_city_by_id,
    get_cities,
    update_city,
)

cities_bp = Blueprint("cities", __name__, url_prefix="/cities")

# Public routes
cities_bp.route("/", methods=["GET"])(get_cities)
cities_bp.route("/<city_id>", methods=["GET"])(get_city_by_id)

# Protected routes
@cities_bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def create_city_protected():
    return create_city()

@cities_bp.route("/<city_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_city_protected(city_id):
    return update_city(city_id)

@cities_bp.route("/<city_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_city_protected(city_id):
    return delete_city(city_id)
