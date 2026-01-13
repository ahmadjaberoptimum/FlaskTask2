from app.extensions import db
from app.models import Book, Library
from app.utils.validators import validate_book_create, validate_book_update


class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors


class NotFoundError(Exception):
    pass


def list_books(filters: dict) -> list[Book]:

    library_id = filters.get("library_id")
    q = filters.get("q")

    query = Book.query

    if library_id:
        query = query.filter(Book.library_id == library_id)

    if q:
        like = f"%{q}%"
        query = query.filter((Book.title.ilike(like)) | (Book.author.ilike(like)))

    return query.order_by(Book.created_at.desc()).all()


def get_book(book_id: int) -> Book:
    book = Book.query.get(book_id)
    if not book:
        raise NotFoundError("Book not found.")
    return book


def create_book(data: dict) -> Book:
    errors = validate_book_create(data)
    if errors:
        raise ValidationError(errors)

    library = Library.query.get(data["library_id"])
    if not library:
        raise NotFoundError("Library not found.")

    book = Book(
        title=data["title"].strip(),
        author=data["author"].strip(),
        library_id=data["library_id"],
    )

    db.session.add(book)
    db.session.commit()
    return book


def update_book(book_id: int, data: dict) -> Book:
    book = Book.query.get(book_id)
    if not book:
        raise NotFoundError("Book not found.")

    errors = validate_book_update(data)
    if errors:
        raise ValidationError(errors)

    if "title" in data and data["title"] is not None:
        book.title = data["title"].strip()

    if "author" in data and data["author"] is not None:
        book.author = data["author"].strip()

    db.session.commit()
    return book


def delete_book(book_id: int) -> None:
    book = Book.query.get(book_id)
    if not book:
        raise NotFoundError("Book not found.")

    db.session.delete(book)
    db.session.commit()


def transfer_book(book_id: int, to_library_id: int) -> Book:
    book = Book.query.get(book_id)
    if not book:
        raise NotFoundError("Book not found.")

    target_lib = Library.query.get(to_library_id)
    if not target_lib:
        raise NotFoundError("Target library not found.")

    book.library_id = to_library_id
    db.session.commit()
    return book
