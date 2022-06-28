from typing import Any
from fastapi import status
from api.models.responses import ApiResponse, Status, Error


class USER_NOT_POCESSED(ApiResponse):
    status: Status = Status.FAILED
    error: Error = Error(type="user", code=100, message="")


DUPLICATED_USER_ERROR = Error(
    type="Duplicated",
    code=110,
    message="User already registred by this email and password",
)


class UserDuplicated(ApiResponse):
    status = Status.FAILED
    error = DUPLICATED_USER_ERROR


create_user: dict[int | str, dict[str, Any]] = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": USER_NOT_POCESSED,
        "description": "USER NOT CREATED",
    },
    status.HTTP_403_FORBIDDEN: {
        "model": UserDuplicated,
        "description": "Credentials Already exist",
    },
}

InvalidCredentialError = Error(
    type="credentials", code=103, message="email or password is incorrect!"
)


class InvalidCredential(ApiResponse):
    status = Status.FAILED
    error = InvalidCredentialError


invalid_credentials: dict[int | str, Any] = {
    status.HTTP_404_NOT_FOUND: {
        "model": InvalidCredential,
        "description": "Invalid credential",
    }
}
