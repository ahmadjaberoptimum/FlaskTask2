from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import User,Book,Library
from app.utils.validators import validate_user_create, validate_user_update


class ValidationError(Exception):
    def __init__(self, errors):
        super().__init__("Validation error")
        self.errors = errors


class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


def create_user(data: dict) -> User:

    errors = validate_user_create(data)
    if errors:
        raise ValidationError(errors)

    if errors:
        raise ValidationError(errors)

    user = User(name=data["name"].strip(), email=data.get("email"))

    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ConflictError("User with this email already exists.")

    return user


def update_user(user_id: int, data: dict) -> User:
    user = User.query.get(user_id)
    if not user:
        raise NotFoundError("User not found.")

    errors = validate_user_update(data)
    if errors:
        raise ValidationError(errors)

    if "name" in data:
        user.name = data["name"].strip()
    if "email" in data:
        user.email = data["email"]

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ConflictError("User with this email already exists.")

    return user

def delete_user(user_id: int) -> None:
    user = User.query.get(user_id)
    if not user:
        raise NotFoundError("User not found.")

    db.session.delete(user)
    db.session.commit()

def list_users () -> list[User]:
    return User.query.all()


def number_of_books (user_id:int) ->int:
    user = User.query.get(user_id)
    if not user:
        raise NotFoundError("User Not Found")
    library = getattr(user,"library",None)
    if not library:
        return 0
    count = Book.query.filter_by(library_id=library.id).count()
    return count

