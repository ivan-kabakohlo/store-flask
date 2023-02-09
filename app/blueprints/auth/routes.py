from flask import jsonify, request
from marshmallow import ValidationError

from app.blueprints.auth import bp
from app.blueprints.auth.controller import (AuthController,
                                            InvalidCredentialsError,
                                            UserExistsError)

auth_controller = AuthController()


@bp.route('/signup', methods=['POST'])
def signup():
    try:
        return auth_controller.signup(request.json)
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422
    except UserExistsError as e:
        return jsonify(e.args[0]), 409


@bp.route('/login', methods=['POST'])
def login():
    try:
        token = auth_controller.login(request.json)
        return jsonify(token)
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422
    except InvalidCredentialsError as e:
        return jsonify(e.args[0]), 401
