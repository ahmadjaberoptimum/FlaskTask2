import pytest
from test.helpers import make_user, make_library, make_book
from app.controllers.users_controller import (
    create_user, update_user, delete_user, list_users,
    number_of_books, ValidationError, NotFoundError, ConflictError
)

def test_create_user_success(app):
    with app.app_context():
        u = create_user({"name": "A", "email": "a@test.com"})
        assert u.id is not None
        assert u.email == "a@test.com"

def test_create_user_validation_error(app):
    with app.app_context():
        with pytest.raises(ValidationError):
            create_user({})

def test_update_user_not_found(app):
    with app.app_context():
        with pytest.raises(NotFoundError):
            update_user(999, {"name": "x"})

def test_update_user_validation_error(app):
    with app.app_context():
        u = make_user("A", "a1@test.com")
        with pytest.raises(ValidationError):
            update_user(u.id, {"name": ""})

def test_delete_user_not_found(app):
    with app.app_context():
        with pytest.raises(NotFoundError):
            delete_user(999)

def test_list_users(app):
    with app.app_context():
        make_user("A", "la@test.com")
        make_user("B", "lb@test.com")
        users = list_users()
        assert len(users) >= 2

def test_user_book_count_zero_if_no_library(app):
    with app.app_context():
        u = make_user("A", "cnt@test.com")
        assert number_of_books(u.id) == 0

def test_create_user_success_and_conflict(app):
    with app.app_context():
        u = create_user({"name": "A", "email": "conf@test.com"})
        assert u.id is not None

        # إذا كنترولر عندك بيرمي ConflictError على نفس الإيميل
        with pytest.raises(ConflictError):
            create_user({"name": "B", "email": "conf@test.com"})

def test_create_user_validation_error(app):
    with app.app_context():
        with pytest.raises(ValidationError):
            create_user({"name": "", "email": ""})

def test_update_user_success(app):
    with app.app_context():
        u = make_user("UU", "uu@test.com")
        updated = update_user(u.id, {"name": "NewName"})
        assert updated.name == "NewName"

def test_update_user_not_found(app):
    with app.app_context():
        with pytest.raises(NotFoundError):
            update_user(999, {"name": "X"})

def test_delete_user_success(app):
    with app.app_context():
        u = make_user("UD", "ud@test.com")
        delete_user(u.id)
        with pytest.raises(NotFoundError):
            number_of_books(u.id)  # user deleted -> NotFoundError

def test_user_book_count_with_library(app):
    with app.app_context():
        u = make_user("UC", "uc@test.com")
        lib = make_library(u.id, "Lib")
        make_book(lib.id, "T1", "A1")
        make_book(lib.id, "T2", "A2")
        assert number_of_books(u.id) == 2
