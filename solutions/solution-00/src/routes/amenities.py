# """
# This module contains the routes for the amenities blueprint
# """

# from flask import Blueprint
# from src.controllers.amenities import (
#     create_amenity,
#     delete_amenity,
#     get_amenity_by_id,
#     get_amenities,
#     update_amenity,
# )

# amenities_bp = Blueprint("amenities", __name__, url_prefix="/amenities")

# amenities_bp.route("/", methods=["GET"])(get_amenities)
# amenities_bp.route("/", methods=["POST"])(create_amenity)

# amenities_bp.route("/<amenity_id>", methods=["GET"])(get_amenity_by_id)
# amenities_bp.route("/<amenity_id>", methods=["PUT"])(update_amenity)
# amenities_bp.route("/<amenity_id>", methods=["DELETE"])(delete_amenity)


"""
This module contains the routes for the amenities blueprint.
"""

"""
This module contains the routes for the amenities blueprint.
"""

from flask import Blueprint
from flask_jwt_extended import jwt_required
from src.decorators import admin_required  # Import the admin_required decorator
from src.controllers.amenities import (
    create_amenity,
    delete_amenity,
    get_amenity_by_id,
    get_amenities,
    update_amenity,
)

amenities_bp = Blueprint("amenities", __name__, url_prefix="/amenities")

# Public routes
amenities_bp.route("/", methods=["GET"])(get_amenities)
amenities_bp.route("/<amenity_id>", methods=["GET"])(get_amenity_by_id)

# Protected routes
@amenities_bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def create_amenity_protected():
    return create_amenity()

@amenities_bp.route("/<amenity_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_amenity_protected(amenity_id):
    return update_amenity(amenity_id)

@amenities_bp.route("/<amenity_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_amenity_protected(amenity_id):
    return delete_amenity(amenity_id)

