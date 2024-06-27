"""
This module contains the routes for the reviews blueprint.
"""

from flask import Blueprint
from flask_jwt_extended import jwt_required
from src.decorators import admin_required  # Import the admin_required decorator
from src.controllers.reviews import (
    create_review,
    delete_review,
    get_reviews_from_place,
    get_reviews_from_user,
    get_review_by_id,
    get_reviews,
    update_review,
)

reviews_bp = Blueprint("reviews", __name__)

# Public routes
reviews_bp.route("/places/<place_id>/reviews", methods=["POST"])(create_review)
reviews_bp.route("/places/<place_id>/reviews")(get_reviews_from_place)
reviews_bp.route("/users/<user_id>/reviews")(get_reviews_from_user)

reviews_bp.route("/reviews", methods=["GET"])(get_reviews)
reviews_bp.route("/reviews/<review_id>", methods=["GET"])(get_review_by_id)

# Protected routes
@reviews_bp.route("/reviews/<review_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_review_protected(review_id):
    return update_review(review_id)

@reviews_bp.route("/reviews/<review_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_review_protected(review_id):
    return delete_review(review_id)
