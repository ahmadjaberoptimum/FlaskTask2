from app.utils.validators import (
    validate_library_create, validate_library_update,
    validate_book_create, validate_book_update
)

def test_validate_library_create_requires_fields():
    errors = validate_library_create({})
    assert "body" in errors

def test_validate_library_update_allows_partial_but_validates_if_present():
    errors = validate_library_update({"name": ""})
    assert "name" in errors

def test_validate_book_create_requires_fields():
    errors = validate_book_create({})
    assert "body" in errors
def test_validate_book_update_partial_validation():
    errors = validate_book_update({"title": ""})
    assert "title" in errors

def test_validate_library_create_ok():
    errors = validate_library_create({"name": "L", "user_id": 1})
    assert errors == {}

def test_validate_book_create_ok():
    errors = validate_book_create({"title": "T", "author": "A", "library_id": 1})
    assert errors == {}
def test_validate_library_create_wrong_types():
    errors = validate_library_create({"name": "X", "user_id": "1"})
    assert "user_id" in errors

def test_validate_book_create_wrong_types():
    errors = validate_book_create({"title": "T", "author": "A", "library_id": "1"})
    assert "library_id" in errors


def test_validate_library_create_wrong_name_type():
    errors = validate_library_create({"name": 123, "user_id": 1})
    assert "name" in errors

def test_validate_library_update_name_none():
    errors = validate_library_update({"name": None})
    assert "name" in errors

def test_validate_book_create_wrong_title_author_types():
    errors = validate_book_create({"title": 1, "author": 2, "library_id": 1})
    assert "title" in errors
    assert "author" in errors

def test_validate_book_update_author_none_and_title_spaces():
    errors = validate_book_update({"title": "   ", "author": None})
    assert "title" in errors
    assert "author" in errors
