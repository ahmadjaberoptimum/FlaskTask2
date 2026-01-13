from flask import Blueprint

root_bp = Blueprint("root", __name__)

@root_bp.get("/")
def home():
    return "Welcome To Library And Books"
