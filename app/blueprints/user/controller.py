from app.repositories.user import UserRepository


class UserController:
    user_repository = UserRepository()

    def read_users(self):
        return self.user_repository.read_all()

    def read_user(self, id: int):
        return self.user_repository.read_by_id(id)
