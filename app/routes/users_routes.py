from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User, Book

from app.controllers.users_controller import (
    ValidationError,
    NotFoundError,
    create_user,
    update_user,
    delete_user,
    list_users,
    number_of_books
)
from app.constants.http_status import(
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND ,
    HTTP_409_CONFLICT ,
    HTTP_422_UNPROCESSABLE_ENTITY ,
    HTTP_500_INTERNAL_SERVER_ERROR
)

users_bp = Blueprint("users", __name__, url_prefix="/users")

def error(msg, code=400):
    return jsonify({"error": msg}), code


@users_bp.get("")
def get_users():
    users = list_users()
    return jsonify([u.to_dict() for u in users]),HTTP_200_OK


@users_bp.post("")
def add_user():
    try:
        data = request.get_json() or {}
        user = create_user(data)
        return jsonify(user.to_dict()),HTTP_201_CREATED
    except ValidationError as e:
        return jsonify({"error" : str(e)}), HTTP_400_BAD_REQUEST


@users_bp.put("/<int:user_id>")
def update_user_route(user_id):
    try:
        data = request.get_json() or {}
        user = update_user(user_id,data)
        return jsonify(user.to_dict()), HTTP_200_OK
    except NotFoundError as e:
        return jsonify({"error" : str(e)}) , HTTP_404_NOT_FOUND
    except ValidationError as e:
        return jsonify({"error" : str(e)}) , HTTP_400_BAD_REQUEST

@users_bp.delete("/<int:user_id>")
def delete_user(user_id):
    try:
        delete_user(user_id)
        return jsonify({"message" : "User Deleted"}), HTTP_200_OK
    except NotFoundError as e:
        return jsonify({"error" : str(e)}) , HTTP_404_NOT_FOUND


@users_bp.get("/<int:user_id>/book_count")
def number_of_books_routes(user_id):
    try:
        count = number_of_books(user_id)
        return jsonify({"user_id": user_id, "book_count": count}), HTTP_200_OK
    except NotFoundError as e:
        return jsonify({"error": str(e)}), HTTP_404_NOT_FOUND
