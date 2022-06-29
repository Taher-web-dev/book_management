from pydantic import BaseModel, Field
from api.models.responses import ApiResponse


class Book(BaseModel):
    isbn: str = Field(..., example="1")
    title: str = Field(..., example="Charlotte's Web ")
    author: str = Field(..., example="Garth Williams")
    publish_date: str = Field(None, example="22-11-2021")
    description: str = Field(
        None,
        example="Charlotte's spiderweb tells of her feelings for a little pig named Wilbur, who simply wants a friend. They also express the love of a girl named Fern, who saved Wilbur's life when he was born the runt of his litter.",
    )
    created_by: str = Field(..., example="2")


class BookModel(ApiResponse):
    data: Book


class DeleteBookSuccessfully(ApiResponse):
    data: str = Field(..., example="Book deleted successfully")


class AllBooksModel(ApiResponse):
    data: list = Field(
        ...,
        example=[
            {
                "isbn": "1",
                "title": "Charlotte's Web ",
                "author": "Garth Williams",
                "publish_date": "22-11-2021",
                "description": "Charlotte's spiderweb tells of her feelings for a little pig named Wilbur, who simply wants a friend. They also express the love of a girl named Fern, who saved Wilbur's life when he was born the runt of his litter.",
                "created_by": "2",
            }
        ],
    )


class BookDetailModel(ApiResponse):
    data: dict = Field(
        ...,
        example={
            "isbn": "1",
            "title": "Charlotte's Web ",
            "author": "Garth Williams",
            "publish_date": "22-11-2021",
            "description": "Charlotte's spiderweb tells of her feelings for a little pig named Wilbur, who simply wants a friend. They also express the love of a girl named Fern, who saved Wilbur's life when he was born the runt of his litter.",
            "created_by": "2",
        },
    )


class FavoritesBook(ApiResponse):
    data: list = Field(..., example=[1, 101, 115, 212])
