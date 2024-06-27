"""
This module contains the routes for the places blueprint
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
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

# Routes requiring authentication
places_bp.route("/", methods=["POST"])(jwt_required()(create_place))
places_bp.route("/<place_id>", methods=["PUT"])(jwt_required()(update_place))
places_bp.route("/<place_id>", methods=["DELETE"])(jwt_required()(delete_place))
