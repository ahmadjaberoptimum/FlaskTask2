from app.extensions import db
from app.models import User, Library, Book

def make_user(name="ahmad", email="ahmad@test.com"):
    u = User(name=name, email=email)
    db.session.add(u)
    db.session.commit()
    return u

def make_library(user_id, name="My Library"):
    lib = Library(name=name, user_id=user_id)
    db.session.add(lib)
    db.session.commit()
    return lib

def make_book(library_id, title="T1", author="A1"):
    b = Book(title=title, author=author, library_id=library_id)
    db.session.add(b)
    db.session.commit()
    return b
