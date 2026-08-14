from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username : str = Field(min_length=1)
    password : str = Field(min_length=8)




class UserResponse(BaseModel):
    username : str