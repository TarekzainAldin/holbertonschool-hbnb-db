"""
This module contains the routes for the countries endpoint
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.controllers.countries import (
    create_country,
    delete_country,
    get_country_by_id,
    get_countries,
    update_country,
)

countries_bp = Blueprint("countries", __name__, url_prefix="/countries")

# Public routes
countries_bp.route("/", methods=["GET"])(get_countries)
countries_bp.route("/<country_id>", methods=["GET"])(get_country_by_id)

# Routes requiring authentication
countries_bp.route("/", methods=["POST"])(jwt_required()(create_country))
countries_bp.route("/<country_id>", methods=["PUT"])(jwt_required()(update_country))
countries_bp.route("/<country_id>", methods=["DELETE"])(jwt_required()(delete_country))
