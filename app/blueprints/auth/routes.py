from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound

from app.blueprints.auth import bp
from app.blueprints.auth.controller import AuthController
from app.custom_exc import UserExists

auth_controller = AuthController()


@bp.route('/signup', methods=['POST'])
def signup():
    try:
        return auth_controller.signup(body=request.json)
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422
    except UserExists as e:
        return jsonify({'message': 'User already exists'}), 409


@bp.route('/login', methods=['POST'])
def login():
    try:
        token = auth_controller.login(body=request.json)
        return jsonify(token)
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422
    except NoResultFound:
        return jsonify({'message': 'Invalid creds'}), 401
