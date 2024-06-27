"""
This module contains the routes for the reviews blueprint
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.controllers.reviews import (
    create_review,
    delete_review,
    get_review_by_id,
    get_reviews,
    update_review,
)
from models.user import User

reviews_bp = Blueprint("reviews", __name__, url_prefix="/reviews")

# Public routes
reviews_bp.route("/", methods=["GET"])(get_reviews)
reviews_bp.route("/<review_id>", methods=["GET"])(get_review_by_id)

# Routes requiring authentication
@reviews_bp.route("/", methods=["POST"])
@jwt_required()
def create_review_route():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    return create_review()

@reviews_bp.route("/<review_id>", methods=["PUT"])
@jwt_required()
def update_review_route(review_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    return update_review(review_id)

@reviews_bp.route("/<review_id>", methods=["DELETE"])
@jwt_required()
def delete_review_route(review_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    return delete_review(review_id)
