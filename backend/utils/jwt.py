import jwt
from .setting import setting
from time import time
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, status
from typing import Optional
from api.models.responses import ApiException
from api.models.api_responses import ACCESS_TOKEN_ERR, INVALID_TOKEN, EXPIRED_TOKEN
from db.main import db


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(
            request
        )
        exception = ApiException(status.HTTP_401_UNAUTHORIZED, ACCESS_TOKEN_ERR)

        if credentials and credentials.scheme == "Bearer":
            decoded_data = decode_jwt(credentials.credentials)
            email = decoded_data.get("email")
            password = decoded_data.get("password")
            users_ref = db.collection("users")
            docs = users_ref.stream()
            user = None
            for doc in docs:
                temp_user = doc.to_dict()
                if (temp_user["email"] == email) & (temp_user["password"] == password):
                    user = temp_user
                    break
            if user["session"]:
                return decoded_data

        raise exception  # No credentials


def sign_jwt(data: dict, expires=setting.jwt_access_expires) -> str:
    payload = {"data": data, "expires": time() + expires}
    return jwt.encode(payload, setting.jwt_secret, algorithm="HS256")


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, setting.jwt_secret, algorithms=["HS256"])
    except:
        raise ApiException(status.HTTP_403_FORBIDDEN, error=INVALID_TOKEN)
    if "data" not in decoded_token or not decoded_token["data"]:
        raise ApiException(status.HTTP_403_FORBIDDEN, error=INVALID_TOKEN)
    if decoded_token["expires"] < time():
        raise ApiException(status.HTTP_410_GONE, EXPIRED_TOKEN)
    return decoded_token["data"]
