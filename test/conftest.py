import os
import tempfile
import pytest

from app import create_app
from app.extensions import db


@pytest.fixture()
def app():

    db_fd, db_path = tempfile.mkstemp()

    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY="test-secret",
    )

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture()
def session(app):
    with app.app_context():
        yield db.session


