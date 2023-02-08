from flask import Blueprint

bp = Blueprint('user', __name__)

from app.blueprints.user import routes
