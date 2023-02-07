from flask import jsonify

from app.extensions import db
from app.models.user import User
from app.user import bp
from app.user.serializers import UserSerializer

user_list_serializer = UserSerializer(many=True)
user_serializer = UserSerializer()


@bp.route('/users', methods=['GET'])
def read_user_list():
    users = db.session.query(User).all()
    return user_list_serializer.dump(users)


@bp.route('/users/<int:id>', methods=['GET'])
def read_user(id):
    user = db.session.query(User).get(id)

    if user is None:
        return jsonify({'message': 'User not found.'}), 404

    return user_serializer.dump(user)
