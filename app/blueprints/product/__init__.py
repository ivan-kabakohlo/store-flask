from flask import Blueprint

bp = Blueprint('product', __name__)

from app.blueprints.product import routes
