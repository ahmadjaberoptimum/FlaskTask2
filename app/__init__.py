from flask import Flask
from dotenv import load_dotenv
load_dotenv()

from .config import Config
from .extensions import db, migrate

from app.routes.users_routes import users_bp
from app.routes.library_routes import libraries_bp
from app.routes.books_routes import books_bp
from app.routes.root_routes import root_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models   
    app.register_blueprint(root_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(libraries_bp)
    app.register_blueprint(books_bp)

    return app
