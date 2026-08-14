from repositories.user_repository import UserRepository
from auth.security import hash_password, verify_password


class UserService:

    def __init__(self, repo: UserRepository):
            self.repo = repo

    def register_user(self, username: str, password: str):
          hashed_password = hash_password(password)
          return self.repo.create_user(username, hashed_password)

    def find_by_username(self, username: str):
          return self.repo.find_by_username(username)

    def authenticate_user(self, username: str, password: str):
          
          user_found = self.find_by_username(username)

          if not user_found:
                return None 

          verificacion = verify_password(password, user_found["password"])

          if not verificacion:
                return None

          return username