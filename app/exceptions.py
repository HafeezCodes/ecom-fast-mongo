from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from google.auth.exceptions import RefreshError
from httplib2.error import ServerNotFoundError
from starlette import status
from starlette.exceptions import HTTPException
from mongoengine.errors import NotUniqueError, ValidationError, OperationError
from pymongo.errors import DuplicateKeyError

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)},
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": exc.errors()[0]["msg"]},
    )

async def invalid_google_access_token_handler(request: Request, exc: RefreshError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Invalid Google Access Token"}
    )

async def server_not_found_error_handler(request: Request, exc: ServerNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)}
    )

# MongoDB Errors
async def not_unique_error_handler(request: Request, exc: NotUniqueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Duplicate key error"}
    )

async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "MongoDB validation error"}
    )

async def operation_error_handler(request: Request, exc: OperationError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Database operation error occurred"}
    )

# General Internal Server Error
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An internal server error occurred"}
    )

# MongoDB Duplicate Key Error
async def duplicate_key_error_handler(request: Request, exc: DuplicateKeyError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Duplicate key error"}
    )