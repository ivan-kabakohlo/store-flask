from flask import jsonify, request
from marshmallow import ValidationError

from app.blueprints.auth import bp
from app.repositories.user import user_repository


@bp.route('/sign_up', methods=['POST'])
def sign_up():
    username = request.json.get('username', None)
    email = request.json.get('email', None)

    is_exists = user_repository.exists(username, email)

    if is_exists:
        return jsonify({'message': 'User already exists.'}), 409

    try:
        return user_repository.create(request.json)
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422
