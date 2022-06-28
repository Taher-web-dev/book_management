from api.models.responses import ApiResponse
from pydantic import BaseModel, Field, EmailStr


class userProfile(BaseModel):
    uid: str = Field(..., example="1")
    first_name: str = Field(None, example="Taher")
    last_name: str = Field(None, example="Haggui")
    email: EmailStr = Field(..., example="example@example.com")
    password: str = Field(..., example="123456")
    favorites: list = Field(..., example=[12, 123, 15])


class UserModel(ApiResponse):
    data: userProfile


class Token(BaseModel):
    token: str = Field(..., example="ac....ea")


class TokenModel(ApiResponse):
    data: Token


class LogoutModel(ApiResponse):
    data: str = Field(..., example="Session log out successfully")
