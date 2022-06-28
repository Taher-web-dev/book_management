from pydantic import BaseModel
from enum import Enum
from typing import Any

# =========API Responses Models=========


class Status(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


class Error(BaseModel):
    type: str
    code: int
    message: str


class ApiResponse(BaseModel):
    """The base Api Response Model"""

    status: Status = Status.SUCCESS
    error: Error | None = None
    data: dict[str, Any] | BaseModel | None = None

    def dict(self, *args, **kwargs) -> dict[str, Any]:
        kwargs.pop("exclude_none")
        return super().dict(*args, exclude_none=True, **kwargs)

    class Config:
        use_enum_values = True

        @staticmethod
        def schema_extra(schema, model) -> None:
            if schema.get("properties")["status"]["default"] == "success":
                schema.get("properties").pop("error")
            if schema.get("properties")["status"]["default"] == "failed":
                schema.get("properties").pop("data")


# ========= Errors Response models ======


class ApiException(Exception):
    """Customized API exception to acts as an ErrorResponse"""

    status_code: int
    error: Error

    def __init__(self, status_code: int, error: Error):
        super().__init__(status_code)
        self.status_code = status_code
        self.error = error
