""" FastApi Main module """
from fastapi import FastAPI, Request
from api.user.router import router as user
from api.book.router import router as book
from starlette.concurrency import iterate_in_threadpool
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from api.models.responses import ApiException, Status, ApiResponse
from api.models.api_responses import token_response
import re

app = FastAPI(
    title="Book Management API",
    description="""### API for Book management test 
  ### Notes:
  * APIs with the 🔒 'lock' icon, require the http header `Authorization: Bearer`.
  * Invoke the login api and use the returned access token in the Authorization form button in the upper right section of this documentation.
  * All the api responses are in application/json format.
  """,
)


@app.on_event("startup")
async def app_startup():
    openapi_schema = app.openapi()
    paths = openapi_schema["paths"]
    for path in paths:
        if re.match(r"^/api/book/all_books(\/)*$", path):
            for method in paths[path]:
                responses = paths[path][method]["responses"]
                if responses.get("401"):
                    responses.pop("401")
                if responses.get("403"):
                    responses.pop("403")
                if responses.get("410"):
                    responses.pop("410")
        if re.match(r"^/api/book/details/\{book_isbn\}(\/)*$", path):
            for method in paths[path]:
                responses = paths[path][method]["responses"]
                if responses.get("401"):
                    responses.pop("401")
                if responses.get("403"):
                    responses.pop("403")
                if responses.get("410"):
                    responses.pop("410")
    app.openapi_schema = openapi_schema


@app.middleware("http")
async def middle(request: Request, call_next):
    """Wrapper function to manage errors"""
    if request.url._url.endswith("/docs") or request.url._url.endswith("/openapi.json"):
        return await call_next(request)
    try:
        response = await call_next(request)
        raw_response = [section async for section in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(raw_response))
    except ApiException as ex:
        response = JSONResponse(
            status_code=ex.status_code,
            content=jsonable_encoder(ApiResponse(status=Status.FAILED, error=ex.error)),
        )

    return response


app.include_router(user, prefix="/api/user", tags=["users"])
app.include_router(book, prefix="/api/book", tags=["books"], responses=token_response)
