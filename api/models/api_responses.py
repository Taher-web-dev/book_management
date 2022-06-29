from email.policy import HTTP
from .responses import Error, ApiResponse, Status
from typing import Any
from fastapi import status

ACCESS_TOKEN_ERR = Error(type="token", code=105, message="Inexistant Access token")
INVALID_TOKEN = Error(type="auth", code=106, message="Invalid access token")
EXPIRED_TOKEN = Error(type="expiration", code=107, message="Expired access token")


class AccessToken(ApiResponse):
    status = Status.FAILED
    error = ACCESS_TOKEN_ERR


class InvalidToken(ApiResponse):
    status = Status.FAILED
    error = INVALID_TOKEN


class ExpiredToken(ApiResponse):
    status = Status.FAILED
    error = EXPIRED_TOKEN


class ValidationError(ApiResponse):
    status = Status.FAILED
    error = Error(code=422, type="validation", message="")


validation_response: dict[int | str, Any] = {
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": ValidationError,
        "description": "Validation Error",
    }
}
token_response: dict[int | str, Any] = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": AccessToken,
        "Description": "Access Token",
    },
    status.HTTP_403_FORBIDDEN: {
        "model": InvalidToken,
        "description": "Invalid Token",
    },
    status.HTTP_410_GONE: {"model": ExpiredToken, "description": "Expired Token"},
}

token_response.update(validation_response)
