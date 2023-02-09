from marshmallow import fields, validate

from app.extensions import ma


class SignupSchema(ma.Schema):
    username = fields.String(required=True,
                             validate=validate.Length(min=4, max=60))
    email = fields.Email(required=True, validate=validate.Email())
    password = fields.String(
        required=True, validate=validate.Length(min=8, max=128))


class LoginSchema(ma.Schema):
    username = fields.String(required=True,
                             validate=validate.Length(min=4, max=60))
    password = fields.String(
        required=True, validate=validate.Length(min=8, max=128))
