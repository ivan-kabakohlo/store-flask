from flask import Blueprint

bp = Blueprint('review', __name__)

from app.blueprints.review import routes
