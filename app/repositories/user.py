from flask_sqlalchemy.model import Model
from marshmallow.schema import Schema
from sqlalchemy import exists

from app.extensions import db
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import user_schema, users_schema


class UserRepository(BaseRepository):
    def __init__(self, User: Model, user_schema: Schema, users_schema: Schema):
        super().__init__(Model=User, schema=user_schema,
                         schema_many=users_schema)
        self.User = User

    def exists(self, username: str, email: str):
        return self.__exists_by_email(email) | \
            self.__exists_by_username(username)

    def __exists_by_email(self, email: str):
        return db.session.query(
            exists().where(self.User.email == email)).scalar()

    def __exists_by_username(self, username: str):
        return db.session.query(
            exists().where(self.User.username == username)).scalar()


user_repository = UserRepository(User, user_schema, users_schema)
