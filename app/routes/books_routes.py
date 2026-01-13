from flask import Blueprint, request, jsonify
from app.constants.http_status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from app.controllers.books_controller import (
    list_books as list_books_controller,
    create_book as create_book_controller,
    update_book as update_book_controller,
    delete_book as delete_book_controller,
    transfer_book as transfer_book_controller,
    ValidationError,
    NotFoundError,
)

books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.get("")
def list_books_route():
    library_id = request.args.get("library_id", type=int)
    q = request.args.get("q", type=str)

    books = list_books_controller({"library_id": library_id, "q": q})
    return jsonify([b.to_dict() for b in books]), HTTP_200_OK


@books_bp.post("")
def create_book_route():
    try:
        data = request.get_json(silent=True) or {}
        book = create_book_controller(data)
        return jsonify(book.to_dict()), HTTP_201_CREATED

    except ValidationError as e:
        return jsonify({"error": "Validation failed", "details": e.errors}), HTTP_400_BAD_REQUEST
    except NotFoundError as e:
        return jsonify({"error": str(e)}), HTTP_404_NOT_FOUND


@books_bp.put("/<int:book_id>")
def update_book_route(book_id: int):
    try:
        data = request.get_json(silent=True) or {}
        book = update_book_controller(book_id, data)
        return jsonify(book.to_dict()), HTTP_200_OK

    except ValidationError as e:
        return jsonify({"error": "Validation failed", "details": e.errors}), HTTP_400_BAD_REQUEST
    except NotFoundError as e:
        return jsonify({"error": str(e)}), HTTP_404_NOT_FOUND


@books_bp.delete("/<int:book_id>")
def delete_book_route(book_id: int):
    try:
        delete_book_controller(book_id)
        return jsonify({"message": "book deleted"}), HTTP_200_OK
    except NotFoundError as e:
        return jsonify({"error": str(e)}), HTTP_404_NOT_FOUND


@books_bp.post("/<int:book_id>/transfer")
def transfer_book_route(book_id: int):
    try:
        data = request.get_json(silent=True) or {}
        to_library_id = data.get("to_library_id")

        if not to_library_id:
            return jsonify({"error": "to_library_id is required"}), HTTP_400_BAD_REQUEST

        book = transfer_book_controller(book_id, int(to_library_id))
        return jsonify({
            "message": "book transferred",
            "book": book.to_dict(),
            "to_library_id": int(to_library_id),
        }), HTTP_200_OK

    except NotFoundError as e:
        return jsonify({"error": str(e)}), HTTP_404_NOT_FOUND
