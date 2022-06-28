from pydantic import BaseSettings


class Setting(BaseSettings):
    jwt_access_expires: int = 3600 * 24
    jwt_algorithm: str = ""
    jwt_secret: str = ""


setting = Setting()
