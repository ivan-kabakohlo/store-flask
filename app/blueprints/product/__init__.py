from flask import Blueprint

bp = Blueprint('product', __name__)

from . import routes
