from fastapi import APIRouter, Depends, status, Path
from utils.jwt import JWTBearer
from api.models.responses import ApiResponse, ApiException, Error
from db.main import db
from .models.requests import UniqueIsbn, BookCreateRequest, BookUpdateRequest
from .models.responses import (
    BookModel,
    Book,
    DeleteBookSuccessfully,
    AllBooksModel,
    BookDetailModel,
)
from .models.exceptions import (
    create_book,
    NOT_OWN_BOOK_ERROR,
    update_book,
    delete_book,
    Book_Not_Found_Error,
    details_book,
)

router = APIRouter()


@router.post("/create", response_model=BookModel, responses=create_book)
async def create_book(
    new_book: BookCreateRequest, credentials=Depends(JWTBearer())
) -> ApiResponse:
    users_ref = db.collection("users")
    docs = users_ref.stream()
    user = None
    for doc in docs:
        temp_user = doc.to_dict()
        if (temp_user["email"] == credentials["email"]) & (
            temp_user["password"] == credentials["password"]
        ):
            user = temp_user
            break
    isbn = None
    try:
        isbn = UniqueIsbn().isbn
        doc_ref = db.collection("books").document(isbn)
        doc_ref.set(
            {
                "isbn": isbn,
                "title": new_book.title,
                "author": new_book.author,
                "publish_date": new_book.publish_date,
                "description": new_book.description,
                "created_by": user["uid"],
            }
        )
    except Exception as ex:
        raise ApiException(
            status.HTTP_406_NOT_ACCEPTABLE,
            error=Error(type="book", code=111, message=str(ex)),
        )
    book = new_book.dict()
    book.update({"isbn": isbn, "created_by": user["uid"]})
    return BookModel(data=Book(**book))


@router.patch("/edit/{book_isbn}", responses=update_book, response_model=BookModel)
async def edit_book(
    book_data: BookUpdateRequest,
    book_isbn: str = Path(..., example="5"),
    credentials=Depends(JWTBearer()),
) -> ApiResponse:
    users_ref = db.collection("users")
    docs = users_ref.stream()
    uid = None
    for doc in docs:
        temp_user = doc.to_dict()
        if (temp_user["email"] == credentials["email"]) & (
            temp_user["password"] == credentials["password"]
        ):
            uid = temp_user["uid"]
            break
    books_ref = db.collection("books")
    docs = books_ref.stream()
    success = False
    book = None
    for doc in docs:
        if doc.id == book_isbn:
            temp_book = doc.to_dict()
            if temp_book["created_by"] != uid:
                raise ApiException(status.HTTP_406_NOT_ACCEPTABLE, NOT_OWN_BOOK_ERROR)
            new_data = book_data.dict()
            doc_ref = db.collection("books").document(doc.id)
            try:
                doc_ref.update(new_data)
                success = True
                book = db.collection("books").document(doc.id).get().to_dict()
            except Exception as ex:
                raise ApiException(
                    status.HTTP_421_MISDIRECTED_REQUEST,
                    error=Error(type="update", code=113, message=str(ex)),
                )
    if success:
        return BookModel(data=Book(**book))
    raise ApiException(status.HTTP_404_NOT_FOUND, Book_Not_Found_Error)


@router.delete(
    "/delete/{book_isbn}", responses=delete_book, response_model=DeleteBookSuccessfully
)
async def delete_book(
    book_isbn: str = Path(..., example="5"), credentials=Depends(JWTBearer())
) -> ApiResponse:
    uid = None
    users_ref = db.collection("users")
    docs = users_ref.stream()
    for doc in docs:
        temp_user = doc.to_dict()
        if (temp_user["email"] == credentials["email"]) & (
            temp_user["password"] == credentials["password"]
        ):
            uid = temp_user["uid"]
    books_ref = db.collection("books")
    docs = books_ref.stream()
    success = False
    for doc in docs:
        if doc.id == book_isbn:
            temp_book = doc.to_dict()
            if temp_book["created_by"] != uid:
                raise ApiException(status.HTTP_406_NOT_ACCEPTABLE, NOT_OWN_BOOK_ERROR)
            try:
                db.collection("books").document(doc.id).delete()
                success = True
            except Exception as ex:
                raise ApiException(
                    status.HTTP_421_MISDIRECTED_REQUEST,
                    error=Error(type="delete", code=116, message=str(ex)),
                )
            break
    if success:
        return DeleteBookSuccessfully(data="Book deleted successfully")
    raise ApiException(status.HTTP_404_NOT_FOUND, Book_Not_Found_Error)


@router.get("/all_books", response_model=AllBooksModel)
async def get_all_books() -> ApiResponse:
    books = []
    books_ref = db.collection("books")
    docs = books_ref.stream()
    for doc in docs:
        books.append(doc.to_dict())
    return AllBooksModel(data=books)


@router.get(
    "/details/{book_isbn}", response_model=BookDetailModel, responses=details_book
)
async def book_detail(book_isbn: str = Path(..., example="3")) -> ApiResponse:
    books_ref = db.collection("books")
    docs = books_ref.stream()
    for doc in docs:
        if doc.id == book_isbn:
            return BookDetailModel(data=doc.to_dict())
    raise ApiException(status.HTTP_404_NOT_FOUND, Book_Not_Found_Error)
