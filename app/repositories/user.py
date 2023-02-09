from flask_sqlalchemy.model import Model
from marshmallow.schema import Schema
from sqlalchemy import and_, exists, or_

from app.extensions import db
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserSchema


class UserRepository(BaseRepository):
    def __init__(self, User: Model, UserSchema: Schema):
        super().__init__(User, UserSchema)
        self.User = User

    def exists(self, username: str, email: str):
        condition = or_(self.User.username == username,
                        self.User.email == email)
        return db.session.query(exists().where(condition)).scalar()

    def read_by_credentials(self, username: str, password: str):
        condition = and_(self.User.username == username,
                         self.User.password == password)
        return db.session.query(User).filter(condition).first()


user_repository = UserRepository(User, UserSchema)
