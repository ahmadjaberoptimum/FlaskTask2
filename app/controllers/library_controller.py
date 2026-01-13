from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import Library, User
from app.utils.validators import validate_library_create, validate_library_update


class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors


class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


def create_library(data: dict) -> Library:
    errors = validate_library_create(data)
    if errors:
        raise ValidationError(errors)

    user = User.query.get(data["user_id"])
    if not user:
        raise NotFoundError("User not found.")

    library = Library(name=data["name"].strip(), user_id=data["user_id"])

    db.session.add(library)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ConflictError("This user already has a library.")

    return library


def get_library(library_id: int) -> Library:
    library = Library.query.get(library_id)
    if not library:
        raise NotFoundError("Library not found.")
    return library


def list_libraries() -> list[Library]:
    return Library.query.all()


def update_library(library_id: int, data: dict) -> Library:
    library = Library.query.get(library_id)
    if not library:
        raise NotFoundError("Library not found.")

    errors = validate_library_update(data)
    if errors:
        raise ValidationError(errors)

    if "name" in data and data["name"] is not None:
        library.name = data["name"].strip()

    db.session.commit()
    return library


def delete_library(library_id: int) -> None:
    library = Library.query.get(library_id)
    if not library:
        raise NotFoundError("Library not found.")

    db.session.delete(library)
    db.session.commit()
