from passlib.context import CryptContext
import jwt
from config.config import settings
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta, timezone

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token (username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {"username": username, "exp":expire}
    token = jwt.encode(payload, settings.secret_key, algorithm="HS256")
    return token

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        username = payload["username"]
        return username
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")