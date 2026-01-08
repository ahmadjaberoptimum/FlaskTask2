from flask import Blueprint, request, jsonify
from .extensions import db
from .models import Library, Book

api_bp = Blueprint("api", __name__)

def error(msg, code=400):
    return jsonify({"error": msg}), code

@api_bp.get('/')
def home ():
    return "Welcome To Library And Books"

@api_bp.get("/libraries")
def list_libraries():
    libs = Library.query.all()
    return jsonify([l.to_dict() for l in libs])

@api_bp.post("/libraries")
def create_library():
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return error("name is required")
    lib = Library(name=name)
    db.session.add(lib)
    db.session.commit()
    return jsonify(lib.to_dict()), 201

@api_bp.put("/libraries/<int:library_id>")
def update_library(library_id):
    lib = Library.query.get(library_id)
    if not lib:
        return error("library not found", 404)

    data = request.get_json() or {}
    name = data.get("name")
    if name:
        lib.name = name
    db.session.commit()
    return jsonify(lib.to_dict())

@api_bp.delete("/libraries/<int:library_id>")
def delete_library(library_id):
    lib = Library.query.get(library_id)
    if not lib:
        return error("library not found", 404)

    db.session.delete(lib)
    db.session.commit()
    return jsonify({"message": "library deleted"})



@api_bp.get("/books")
def list_books():
    library_id = request.args.get("library_id", type=int)
    q = request.args.get("q", type=str)

    query = Book.query

    if library_id:
        query = query.filter(Book.library_id == library_id)

    if q:
        like = f"%{q}%"
        query = query.filter((Book.title.ilike(like)) | (Book.author.ilike(like)))

    books = query.order_by(Book.created_at.desc()).all()
    return jsonify([b.to_dict() for b in books])

@api_bp.post("/books")
def create_book():
    data = request.get_json() or {}
    title = data.get("title")
    author = data.get("author")
    library_id = data.get("library_id")

    if not title or not author or not library_id:
        return error("title, author, library_id are required")

    lib = Library.query.get(library_id)
    if not lib:
        return error("library_id not found", 404)

    book = Book(title=title, author=author, library_id=library_id)
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict()), 201

@api_bp.put("/books/<int:book_id>")
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return error("book not found", 404)

    data = request.get_json() or {}
    if "title" in data and data["title"]:
        book.title = data["title"]
    if "author" in data and data["author"]:
        book.author = data["author"]

    if "library_id" in data and data["library_id"]:
        lib = Library.query.get(data["library_id"])
        if not lib:
            return error("library_id not found", 404)
        book.library_id = data["library_id"]

    db.session.commit()
    return jsonify(book.to_dict())

@api_bp.delete("/books/<int:book_id>")
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return error("book not found", 404)

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "book deleted"})


@api_bp.get("/libraries/<int:library_id>/books")
def library_books(library_id):
    lib = Library.query.get(library_id)
    if not lib:
        return error("library not found", 404)

    return jsonify({
        "library": lib.to_dict(),
        "books": [b.to_dict() for b in lib.books]
    })
