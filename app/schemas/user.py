from marshmallow import fields, validate

from app.extensions import ma
from app.models.user import User


class UserSchema(ma.Schema):
    username = fields.String(
        required=True, validate=validate.Length(min=4, max=60))
    email = fields.Email(required=True, validate=validate.Email())
    password = fields.String(
        required=True, validate=validate.Length(min=8, max=128))
    avatar_url = fields.Url(required=False)
    bio = fields.String(required=False, validate=validate.Length(max=2000))
    birthday = fields.Date(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'avatar_url',
                  'bio', 'birthday', 'created_at', 'updated_at')
        load_only = ['password']
