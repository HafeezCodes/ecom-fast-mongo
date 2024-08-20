from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from google.auth.exceptions import RefreshError
from httplib2.error import ServerNotFoundError
from starlette.exceptions import HTTPException
from mongoengine.errors import NotUniqueError, ValidationError, OperationError
from pymongo.errors import DuplicateKeyError

from app.constants import constants
from app.routers import user
from app.database import connect_db, disconnect_db
# from app.utils.json_encoder import custom_json_response
from app.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    invalid_google_access_token_handler,
    server_not_found_error_handler,
    not_unique_error_handler,
    validation_error_handler,
    operation_error_handler,
    general_exception_handler,
    duplicate_key_error_handler
)

# Define the lifespan context function
async def lifespan_context(app: FastAPI):
    # Startup
    await connect_db()
    yield
    # Shutdown
    await disconnect_db()

# Create the FastAPI app instance
app = FastAPI(lifespan=lifespan_context)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=constants.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router)
# app.include_router(label.router)
# app.include_router(note.router)

# Exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(RefreshError, invalid_google_access_token_handler)
app.add_exception_handler(ServerNotFoundError, server_not_found_error_handler)
app.add_exception_handler(NotUniqueError, not_unique_error_handler)
app.add_exception_handler(ValidationError, validation_error_handler)
app.add_exception_handler(OperationError, operation_error_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(DuplicateKeyError, duplicate_key_error_handler)

# Use custom JSON response globally
# app.json_response_class = custom_json_response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
