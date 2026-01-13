from flask import Blueprint, request, jsonify
from app.constants.http_status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from app.controllers.library_controller import (
    create_library,
    update_library,
    delete_library,
    list_libraries,
    get_library,
    ValidationError,
    NotFoundError,
    ConflictError,
)

libraries_bp = Blueprint("libraries", __name__, url_prefix="/libraries")


@libraries_bp.get("")
def list_libraries_route():
    libs = list_libraries()
    return jsonify([l.to_dict() for l in libs]), HTTP_200_OK


@libraries_bp.get("/<int:library_id>")
def get_library_route(library_id: int):
    try:
        lib = get_library(library_id)
        return jsonify(lib.to_dict()), HTTP_200_OK
    except NotFoundError as e:
        return jsonify({"error": str(e)}), HTTP_404_NOT_FOUND


@libraries_bp.post("")
def create_library_route():
    try:
        data = request.get_json(silent=True) or {}
        lib = create_library(data)
        return jsonify(lib.to_dict()), HTTP_201_CREATED

    except ValidationError as e:
        return jsonify({"error": "Validation failed", "details": e.errors}), HTTP_400_BAD_REQUEST
    except NotFoundError as e:
        return jsonify({"error": str(e)}), HTTP_404_NOT_FOUND
    except ConflictError as e:
        return jsonify({"error": str(e)}), HTTP_409_CONFLICT


@libraries_bp.put("/<int:library_id>")
def update_library_route(library_id: int):
    try:
        data = request.get_json(silent=True) or {}
        lib = update_library(library_id, data)
        return jsonify(lib.to_dict()), HTTP_200_OK

    except ValidationError as e:
        return jsonify({"error": "Validation failed", "details": e.errors}), HTTP_400_BAD_REQUEST
    except NotFoundError as e:
        return jsonify({"error": str(e)}), HTTP_404_NOT_FOUND


@libraries_bp.delete("/<int:library_id>")
def delete_library_route(library_id: int):
    try:
        delete_library(library_id)
        return jsonify({"message": "library deleted"}), HTTP_200_OK
    except NotFoundError as e:
        return jsonify({"error": str(e)}), HTTP_404_NOT_FOUND


@libraries_bp.get("/<int:library_id>/books")
def library_books_route(library_id: int):
    try:
        lib = get_library(library_id)
        return jsonify({
            "library": lib.to_dict(),
            "books": [b.to_dict() for b in lib.books],
        }), HTTP_200_OK
    except NotFoundError as e:
        return jsonify({"error": str(e)}), HTTP_404_NOT_FOUND
