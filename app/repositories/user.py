from flask_sqlalchemy.model import Model
from marshmallow.schema import Schema

from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import user_schema, users_schema


class UserRepository(BaseRepository):
    def __init__(self, User: Model, user_schema: Schema, users_schema: Schema):
        super().__init__(Model=User, schema=user_schema, schema_many=users_schema)


user_repository = UserRepository(User, user_schema, users_schema)
