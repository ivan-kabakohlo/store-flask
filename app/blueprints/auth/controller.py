from app.repositories.user import user_repository
from app.schemas.auth import LoginSchema, SignupSchema
from app.schemas.user import UserSchema


class UserExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class AuthController:
    user_repository = user_repository
    user_schema = UserSchema()
    login_schema = LoginSchema()
    signup_schema = SignupSchema()

    def signup(self, body: dict() = {}):
        self.signup_schema.load(body)

        username = body['username']
        email = body['email']

        if self.user_repository.exists(username, email):
            raise UserExistsError({'message': 'User already exists.'})

        return user_repository.create(body)

    def login(self, body: dict() = {}):
        self.login_schema.load(body)

        user = user_repository.read_by_credentials(**body)

        if not user:
            raise InvalidCredentialsError({'message': 'Invalid credentials.'})

        user = self.user_schema.dump(user)


auth_controller = AuthController()
