from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import user_schema, users_schema


class UserRepository(BaseRepository):
    def __init__(self, Model, schema, schema_many):
        super().__init__(Model, schema, schema_many)


user_repository = UserRepository(User, user_schema, users_schema)
