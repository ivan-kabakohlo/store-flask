from flask_jwt_extended import jwt_required

from app.blueprints.user import bp
from app.repositories.user import user_repository


@bp.route('/users', methods=['GET'])
@jwt_required()
def read_user_list():
    return user_repository.read_all()


@bp.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def read_user(id: int):
    return user_repository.read_by_id(id)
