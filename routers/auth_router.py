from fastapi import APIRouter, Depends, HTTPException
from models.user_model import UserCreate, UserResponse
from repositories.user_repository import UserRepository, UserManagerSQLite
from services.user_service import UserService
from auth.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

user_manager = UserManagerSQLite()

def get_user_repository():
    return user_manager

def get_user_service(repo: UserRepository = Depends(get_user_repository)):
    return UserService(repo)




@router.post("/register", response_model= UserResponse)
def register_user(user: UserCreate, service: UserService = Depends(get_user_service)):

    new_user = service.register_user(user.username, user.password)

    return {
        "username":new_user["username"]
    }

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm= Depends(), service: UserService = Depends(get_user_service)):
    authenticated_user = service.authenticate_user(form_data.username, form_data.password)

    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(authenticated_user)

    return {
        "access_token": access_token,
        "token_type": "bearer" 
    }