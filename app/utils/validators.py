import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_user_create(data: dict):
    errors = {}

    name = data.get("name")
    email = data.get("email")

    if not isinstance(name, str) or not name.strip():
        errors["name"] = "name is required and must be a non-empty string."

    if email is not None:
        if not isinstance(email, str) or not EMAIL_RE.match(email):
            errors["email"] = "email must be a valid email address."

    return errors


def validate_user_update(data: dict):
    errors = {}

    if not isinstance(data, dict) or not data:
        errors["payload"] = "request body must include at least one field."

    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            errors["name"] = "name must be a non-empty string."

    if "email" in data:
        email = data["email"]
        if email is not None and (not isinstance(email, str) or not EMAIL_RE.match(email)):
            errors["email"] = "email must be a valid email address or null."

    return errors


# =========================
# Library Validators
# =========================

def validate_library_create(data: dict) -> dict:
    errors = {}

    if not data:
        errors["body"] = "Request body is required."
        return errors

    name = data.get("name")
    user_id = data.get("user_id")

    if not name or not isinstance(name, str) or not name.strip():
        errors["name"] = "Library name is required."

    if not user_id or not isinstance(user_id, int):
        errors["user_id"] = "Valid user_id is required."

    return errors


def validate_library_update(data: dict) -> dict:
    errors = {}

    if not data:
        errors["body"] = "Request body is required."
        return errors

    if "name" in data:
        name = data.get("name")
        if not name or not isinstance(name, str) or not name.strip():
            errors["name"] = "Library name must be a non-empty string."

    return errors




# =========================
# Book Validators
# =========================

def validate_book_create(data: dict) -> dict:
    errors = {}

    if not data:
        errors["body"] = "Request body is required."
        return errors

    title = data.get("title")
    author = data.get("author")
    library_id = data.get("library_id")

    if not title or not isinstance(title, str) or not title.strip():
        errors["title"] = "Book title is required."

    if not author or not isinstance(author, str) or not author.strip():
        errors["author"] = "Book author is required."

    if not library_id or not isinstance(library_id, int):
        errors["library_id"] = "Valid library_id is required."

    return errors


def validate_book_update(data: dict) -> dict:
    errors = {}

    if not data:
        errors["body"] = "Request body is required."
        return errors

    if "title" in data:
        title = data.get("title")
        if not title or not isinstance(title, str) or not title.strip():
            errors["title"] = "Book title must be a non-empty string."

    if "author" in data:
        author = data.get("author")
        if not author or not isinstance(author, str) or not author.strip():
            errors["author"] = "Book author must be a non-empty string."

    return errors
