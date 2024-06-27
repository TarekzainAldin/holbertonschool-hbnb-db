"""
This module contains the routes for the reviews blueprint
"""


from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.controllers.reviews import (
    create_review,
    delete_review,
    get_review_by_id,
    get_reviews,
    update_review,
)

reviews_bp = Blueprint("reviews", __name__, url_prefix="/reviews")

# Public routes
reviews_bp.route("/", methods=["GET"])(get_reviews)
reviews_bp.route("/<review_id>", methods=["GET"])(get_review_by_id)

# Routes requiring authentication
reviews_bp.route("/", methods=["POST"])(jwt_required()(create_review))
reviews_bp.route("/<review_id>", methods=["PUT"])(jwt_required()(update_review))
reviews_bp.route("/<review_id>", methods=["DELETE"])(jwt_required()(delete_review))
