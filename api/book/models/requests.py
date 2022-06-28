from pydantic import BaseModel, Field
import pickle


class UniqueIsbn:
    isbn = "0"
    try:
        with open("./encodedisbn", "rb") as f:
            try:
                isbn = pickle.load(f)
            except:
                pass
    except:
        pass

    def __init__(self):
        self.__class__.isbn = str(int(self.__class__.isbn) + 1)
        with open("./encodedisbn", "wb") as f:
            pickle.dump(self.__class__.isbn, f)


class BookCreateRequest(BaseModel):
    title: str = Field(..., example="Charlotte's Web ")
    author: str = Field(..., example="Garth Williams")
    publish_date: str = Field(None, example="15-12-2021")
    description: str = Field(
        None,
        example="Charlotte's spiderweb tells of her feelings for a little pig named Wilbur, who simply wants a friend. They also express the love of a girl named Fern, who saved Wilbur's life when he was born the runt of his litter.",
    )


class BookUpdateRequest(BaseModel):
    title: str = Field(None, example="Charlotte's Web ")
    author: str = Field(None, example="Garth Williams")
    publish_date: str = Field(None, example="15-12-2021")
    description: str = Field(
        None,
        example="Charlotte's spiderweb tells of her feelings for a little pig named Wilbur, who simply wants a friend. They also express the love of a girl named Fern, who saved Wilbur's life when he was born the runt of his litter.",
    )
