"""
This module contains the routes for the places blueprint.
"""

from flask import Blueprint
from flask_jwt_extended import jwt_required
from src.decorators import admin_required  # Import the admin_required decorator
from src.controllers.places import (
    create_place,
    delete_place,
    get_place_by_id,
    get_places,
    update_place,
)

places_bp = Blueprint("places", __name__, url_prefix="/places")

# Public routes
places_bp.route("/", methods=["GET"])(get_places)
places_bp.route("/<place_id>", methods=["GET"])(get_place_by_id)

# Protected routes
@places_bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def create_place_protected():
    return create_place()

@places_bp.route("/<place_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_place_protected(place_id):
    return update_place(place_id)

@places_bp.route("/<place_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_place_protected(place_id):
    return delete_place(place_id)
