from flask_jwt_extended import create_access_token
from sqlalchemy.exc import NoResultFound

from app.custom_exc import UserExists
from app.repositories.user import UserRepository
from app.schemas.auth import LoginSchema, SignupSchema
from app.schemas.user import UserSchema


class AuthController:
    user_repository = UserRepository()
    user_schema = UserSchema()
    login_schema = LoginSchema()
    signup_schema = SignupSchema()

    def signup(self, body: dict):
        self.signup_schema.load(body)

        username = body['username']
        email = body['email']

        if self.user_repository.exists(username, email):
            raise UserExists

        return self.user_repository.create(body)

    def login(self, body: dict):
        self.login_schema.load(body)

        user = self.user_repository.read_by_credentials(**body)

        if user is None:
            raise NoResultFound

        user = self.user_schema.dump(user)

        access_token = create_access_token(identity=user)

        return {'access_token': access_token}
