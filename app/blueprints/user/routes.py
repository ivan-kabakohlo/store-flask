from flask import jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import NoResultFound

from app.blueprints.user import bp
from app.blueprints.user.controller import UserController

user_controller = UserController()


@bp.route('/users', methods=['GET'])
@jwt_required()
def read_users():
    return user_controller.read_users()


@bp.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def read_user(id: int):
    try:
        return user_controller.read_user(id)
    except NoResultFound:
        return jsonify({'message': 'User not found'}), 404
