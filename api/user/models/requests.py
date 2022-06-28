from pydantic import BaseModel, Field, EmailStr
import pickle


class Uniqueuid:
    uid = "0"
    try:
        with open("./uidencoding", "rb") as f:
            try:
                uid = pickle.load(f)
            except:
                pass
    except:
        pass

    def __init__(self):
        self.__class__.uid = str(int(self.__class__.uid) + 1)
        with open("./uidencoding", "wb") as f:
            pickle.dump(self.__class__.uid, f)


class UserCreateRequest(BaseModel):
    first_name: str = Field(None, example="Taher")
    last_name: str = Field(None, example="Haggui")
    email: EmailStr = Field(..., example="example@example.com")
    password: str = Field(..., example="123456")
    favorites: list = Field(..., example=[12, 123, 15])
