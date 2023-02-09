from app.blueprints.user import bp
from app.repositories.user import user_repository


@bp.route('/users', methods=['GET'])
def read_user_list():
    return user_repository.read_all()


@bp.route('/users/<int:id>', methods=['GET'])
def read_user(id: int):
    return user_repository.read_by_id(id)
