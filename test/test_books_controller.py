import pytest
from test.helpers import make_user, make_library, make_book
from app.controllers.books_controller import (
    list_books, get_book, create_book, update_book, delete_book, transfer_book,
    ValidationError, NotFoundError
)

def test_list_books_filters_and_search(app):
    with app.app_context():
        u = make_user()
        lib1 = make_library(u.id, "L1")
        lib2 = make_library(u.id, "L2")
        b1 = make_book(lib1.id, title="Python 101", author="Ahmad")
        make_book(lib1.id, title="Flask Book", author="Someone")
        make_book(lib2.id, title="Other", author="Ahmad")

        # filter by library
        books = list_books({"library_id": lib1.id, "q": None})
        assert all(b.library_id == lib1.id for b in books)

        # search by q
        books = list_books({"library_id": None, "q": "python"})
        assert any("Python" in b.title for b in books)

def test_get_book_not_found(app):
    with app.app_context():
        with pytest.raises(NotFoundError):
            get_book(999)

def test_create_book_validation_error(app):
    with app.app_context():
        with pytest.raises(ValidationError):
            create_book({})

def test_update_book_not_found(app):
    with app.app_context():
        with pytest.raises(NotFoundError):
            update_book(999, {"title": "x"})

def test_update_book_validation_error(app):
    with app.app_context():
        u = make_user()
        lib = make_library(u.id)
        b = make_book(lib.id)
        with pytest.raises(ValidationError):
            update_book(b.id, {"title": ""})

def test_delete_book_not_found(app):
    with app.app_context():
        with pytest.raises(NotFoundError):
            delete_book(999)

def test_transfer_book_book_not_found(app):
    with app.app_context():
        u = make_user()
        lib = make_library(u.id)
        with pytest.raises(NotFoundError):
            transfer_book(999, lib.id)

def test_transfer_book_target_not_found(app):
    with app.app_context():
        u = make_user()
        lib = make_library(u.id)
        b = make_book(lib.id)
        with pytest.raises(NotFoundError):
            transfer_book(b.id, 999)
def test_list_books_no_filters(app):
    with app.app_context():
        u = make_user("U1", "u1_list@test.com")
        lib = make_library(u.id, "L1")
        make_book(lib.id, "Python 101", "Ahmad")
        make_book(lib.id, "Flask 101", "Wafaa")
        result = list_books({"library_id": None, "q": None})
        assert len(result) >= 2

def test_list_books_filter_and_search(app):
    with app.app_context():
        u1 = make_user("U2", "u2_list@test.com")
        u2 = make_user("U3", "u3_list@test.com")
        lib1 = make_library(u1.id, "L1")
        lib2 = make_library(u2.id, "L2")
        make_book(lib1.id, "Clean Code", "Robert")
        make_book(lib2.id, "Python Tricks", "Dan")

        filtered = list_books({"library_id": lib2.id, "q": None})
        assert all(b.library_id == lib2.id for b in filtered)

        searched = list_books({"library_id": None, "q": "python"})
        assert any("Python" in b.title for b in searched)

def test_get_book_not_found(app):
    with app.app_context():
        with pytest.raises(NotFoundError):
            get_book(999)

def test_create_book_validation_and_library_not_found(app):
    with app.app_context():
        with pytest.raises(ValidationError):
            create_book({})

        with pytest.raises(NotFoundError):
            create_book({"title": "T", "author": "A", "library_id": 999})

def test_update_book_not_found_and_validation(app):
    with app.app_context():
        with pytest.raises(NotFoundError):
            update_book(999, {"title": "X"})

        u = make_user("U4", "u4@test.com")
        lib = make_library(u.id, "L")
        b = make_book(lib.id, "Old", "Auth")

        with pytest.raises(ValidationError):
            update_book(b.id, {"title": ""})

def test_delete_book_not_found(app):
    with app.app_context():
        with pytest.raises(NotFoundError):
            delete_book(999)

def test_transfer_book_book_not_found_and_target_not_found(app):
    with app.app_context():
        u = make_user("U5", "u5@test.com")
        lib = make_library(u.id, "L")
        with pytest.raises(NotFoundError):
            transfer_book(999, lib.id)

        b = make_book(lib.id, "T", "A")
        with pytest.raises(NotFoundError):
            transfer_book(b.id, 999)


def test_get_book_success(app):
    with app.app_context():
        u = make_user("BG", "bg@test.com")
        lib = make_library(u.id, "Lib")
        book = make_book(lib.id, "T", "A")
        found = get_book(book.id)
        assert found.id == book.id

def test_update_book_updates_title_and_author(app):
    with app.app_context():
        u = make_user("BU", "bu@test.com")
        lib = make_library(u.id, "Lib")
        book = make_book(lib.id, "Old", "OldA")

        updated = update_book(book.id, {"title": "New", "author": "NewA"})
        assert updated.title == "New"
        assert updated.author == "NewA"

def test_delete_book_success(app):
    with app.app_context():
        u = make_user("BD", "bd@test.com")
        lib = make_library(u.id, "Lib")
        book = make_book(lib.id, "T", "A")

        delete_book(book.id)
        with pytest.raises(NotFoundError):
            get_book(book.id)

def test_transfer_book_success(app):
    with app.app_context():
        u1 = make_user("BT1", "bt1@test.com")
        u2 = make_user("BT2", "bt2@test.com")
        lib1 = make_library(u1.id, "L1")
        lib2 = make_library(u2.id, "L2")
        book = make_book(lib1.id, "T", "A")

        moved = transfer_book(book.id, lib2.id)
        assert moved.library_id == lib2.id
