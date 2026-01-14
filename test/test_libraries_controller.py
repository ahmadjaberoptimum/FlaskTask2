import pytest
from app.controllers.library_controller import (
    create_library, update_library, delete_library, get_library,
    ValidationError, NotFoundError, ConflictError
)
from test.helpers import make_user,make_library

def test_create_library_success(app):
    with app.app_context():
        user = make_user()
        lib = create_library({"name": "Main", "user_id": user.id})
        assert lib.id is not None
        assert lib.name == "Main"
        assert lib.user_id == user.id

def test_create_library_validation_error(app):
    with app.app_context():
        with pytest.raises(ValidationError):
            create_library({"name": "", "user_id": 1})

def test_create_library_user_not_found(app):
    with app.app_context():
        with pytest.raises(NotFoundError):
            create_library({"name": "X", "user_id": 999})

def test_create_library_conflict_one_library_per_user(app):
    with app.app_context():
        user = make_user()
        create_library({"name": "L1", "user_id": user.id})
        with pytest.raises(ConflictError):
            create_library({"name": "L2", "user_id": user.id})

def test_update_library_success(app):
    from test.helpers import make_library
    with app.app_context():
        user = make_user()
        lib = make_library(user.id, "Old")
        updated = update_library(lib.id, {"name": "New"})
        assert updated.name == "New"

def test_delete_library_not_found(app):
    with app.app_context():
        with pytest.raises(NotFoundError):
            delete_library(999)


def test_get_library_success(app):
    with app.app_context():
        u = make_user("LG", "lg@test.com")
        lib = make_library(u.id, "Lib")
        found = get_library(lib.id)
        assert found.id == lib.id

def test_update_library_no_name_key_keeps_same(app):
    with app.app_context():
        u = make_user("LU", "lu@test.com")
        lib = make_library(u.id, "Old")
        updated = update_library(lib.id, {})  
        assert updated.name == "Old"

def test_delete_library_success(app):
    with app.app_context():
        u = make_user("LD", "ld@test.com")
        lib = make_library(u.id, "Lib")
        delete_library(lib.id)
        with pytest.raises(NotFoundError):
            get_library(lib.id)
