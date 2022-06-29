""" User management apis """
from fastapi import APIRouter, Depends, status, Body
from .models.requests import UserCreateRequest, Uniqueuid
from .models.responses import UserModel, TokenModel, LogoutModel, userProfile
from .models.exceptions import (
    create_user,
    InvalidCredentialError,
    invalid_credentials,
    DUPLICATED_USER_ERROR,
)
from api.models.responses import Error, ApiException, ApiResponse
from utils.password import hash_password, verify_password
from db.main import db
from pydantic import EmailStr
from utils.jwt import sign_jwt, JWTBearer
from api.models.api_responses import token_response

router = APIRouter()


@router.post("/create", response_model=UserModel, responses=create_user)
async def register_user(new_user: UserCreateRequest) -> ApiResponse:
    users_ref = db.collection("users")
    docs = users_ref.stream()
    user_exist = False
    for doc in docs:
        temp_user = doc.to_dict()
        try:
            verify_password(temp_user["password"], new_user.password)
        except:
            continue
        if temp_user["email"] == new_user.email:
            user_exist = True
            break
    if user_exist:
        raise ApiException(status.HTTP_403_FORBIDDEN, DUPLICATED_USER_ERROR)
    uid = None
    try:
        uid = Uniqueuid().uid
        doc_ref = db.collection("users").document(uid)
        doc_ref.set(
            {
                "uid": uid,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email,
                "password": hash_password(new_user.password),
                "favorites": new_user.favorites,
                "session": False,
            }
        )
    except Exception as ex:
        raise ApiException(
            status.HTTP_401_UNAUTHORIZED,
            error=Error(type="user", code=100, message=str(ex)),
        )
    current_user = new_user.dict()
    current_user.update({"uid": uid})
    return UserModel(data=userProfile(**current_user))


@router.post("/login", response_model=TokenModel, responses=invalid_credentials)
async def login_user(
    email: EmailStr = Body(..., example="example@example.com"),
    password: str = Body(..., example="123456"),
) -> ApiResponse:
    """Login and generate a token"""
    users_ref = db.collection("users")
    docs = users_ref.stream()
    user = None
    for doc in docs:
        temp_user = doc.to_dict()
        try:
            verify_password(temp_user["password"], password)
        except:
            continue
        if temp_user["email"] == email:
            doc_ref = db.collection("users").document(doc.id)
            doc_ref.update({"session": True})
            user = doc.to_dict()
            break
    if user:
        token = sign_jwt({"email": email, "password": user["password"]})
        return TokenModel(data={"token": token})

    raise ApiException(status.HTTP_404_NOT_FOUND, InvalidCredentialError)


@router.post("/logout", responses=token_response, response_model=LogoutModel)
async def logout_user(credentials=Depends(JWTBearer())) -> ApiResponse:
    users_ref = db.collection("users")
    docs = users_ref.stream()
    for doc in docs:
        temp_user = doc.to_dict()
        if (temp_user["email"] == credentials["email"]) & (
            temp_user["password"] == credentials["password"]
        ):
            doc_ref = db.collection("users").document(doc.id)
            doc_ref.update({"session": False})
            break
    return LogoutModel(data="User logged out successfully.")
