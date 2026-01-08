from flask import Flask
from dotenv import load_dotenv
from .config import Config
from .extensions import db, migrate
from .routes import api_bp


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api_bp)

    return app
