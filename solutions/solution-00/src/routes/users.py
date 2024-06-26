# """
# This module contains the routes for the users endpoints.
# """

# from flask import Blueprint
# from src.controllers.users import (
#     create_user,
#     delete_user,
#     get_user_by_id,
#     get_users,
#     update_user,
# )

# users_bp = Blueprint("users", __name__, url_prefix="/users")

# users_bp.route("/", methods=["GET"])(get_users)
# users_bp.route("/", methods=["POST"])(create_user)

# users_bp.route("/<user_id>", methods=["GET"])(get_user_by_id)
# users_bp.route("/<user_id>", methods=["PUT"])(update_user)
# users_bp.route("/<user_id>", methods=["DELETE"])(delete_user)
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.controllers.users import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
)

users_bp = Blueprint("users", __name__, url_prefix="/users")

# Unprotected endpoints
users_bp.route("/", methods=["GET"])(get_users)
users_bp.route("/", methods=["POST"])(create_user)

# Protected endpoints requiring JWT authentication
@users_bp.route("/<user_id>", methods=["GET"])
@jwt_required()
def get_user_by_id_protected(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    return get_user_by_id(user_id)

@users_bp.route("/<user_id>", methods=["PUT"])
@jwt_required()
def update_user_protected(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    return update_user(user_id, request.json)

@users_bp.route("/<user_id>", methods=["DELETE"])
@jwt_required()
def delete_user_protected(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    return delete_user(user_id)
