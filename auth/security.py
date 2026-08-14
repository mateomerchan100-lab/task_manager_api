from passlib.context import CryptContext
import jwt
from config.config import settings
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token (username: str) -> str:
    payload = {"username": username}
    token = jwt.encode(payload, settings.secret_key, algorithm="HS256")
    return token

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    username = payload["username"]
    return username
