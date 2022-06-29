from api.models.responses import ApiResponse, Status, Error
from typing import Any
from fastapi import status


class BookNotProcessed(ApiResponse):
    status = Status.FAILED
    error = Error(type="book", code=111, message="")


create_book: dict[int | str, Any] = {
    status.HTTP_406_NOT_ACCEPTABLE: {
        "model": BookNotProcessed,
        "description": "Book not processed",
    }
}

NOT_OWN_BOOK_ERROR = Error(
    type="ownership", code=112, message="You don't own this book"
)


class BookOwnership(ApiResponse):
    status = Status.FAILED
    error = NOT_OWN_BOOK_ERROR


class NotUpdated(ApiResponse):
    status = Status.FAILED
    error = Error(type="update", code=113, message="")


Book_Not_Found_Error = Error(
    type="book", code=115, message="The isbn provided not match any saved book."
)


class BookNotFound(ApiResponse):
    status = Status.FAILED
    error = Book_Not_Found_Error


update_book: dict[int | str, Any] = {
    status.HTTP_405_METHOD_NOT_ALLOWED: {
        "model": BookOwnership,
        "description": "Book Ownership",
    },
    status.HTTP_421_MISDIRECTED_REQUEST: {
        "model": NotUpdated,
        "description": "Book not updated",
    },
    status.HTTP_404_NOT_FOUND: {
        "model": BookNotFound,
        "description": "Book Not Available",
    },
}


class BookNotDeleted(ApiResponse):
    status = Status.FAILED
    error = Error(type="delete", code=116, message="")


delete_book: dict[int | str, Any] = {
    status.HTTP_405_METHOD_NOT_ALLOWED: {
        "model": BookOwnership,
        "description": "Book Ownership",
    },
    status.HTTP_421_MISDIRECTED_REQUEST: {
        "model": BookNotDeleted,
        "description": "Book not deleted",
    },
    status.HTTP_404_NOT_FOUND: {
        "model": BookNotFound,
        "description": "Book Not Available",
    },
}

details_book: dict[str | int, Any] = {
    status.HTTP_404_NOT_FOUND: {
        "model": BookNotFound,
        "description": "Book Not Available",
    }
}

book_to_favorites: dict[str | int, Any] = {
    status.HTTP_404_NOT_FOUND: {
        "model": BookNotFound,
        "description": "Book Not Available",
    },
    status.HTTP_421_MISDIRECTED_REQUEST: {
        "model": NotUpdated,
        "description": "User not updated",
    },
}


class NotFavoriteBook(ApiResponse):
    status = Status.FAILED
    error = Error(
        type="not favorites", code=117, message="book_isbn not in favorite list"
    )


delete_favorite_book: dict[int | str, Any] = {
    status.HTTP_400_BAD_REQUEST: {
        "model": NotFavoriteBook,
        "description": "Book already not in favorites books",
    },
    status.HTTP_421_MISDIRECTED_REQUEST: {
        "model": NotUpdated,
        "description": "User not updated",
    },
}
