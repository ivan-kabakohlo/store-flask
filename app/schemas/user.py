from app.extensions import ma
from app.models.user import User


class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar_url',
                  'bio', 'birthday', 'created_at', 'updated_at')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
