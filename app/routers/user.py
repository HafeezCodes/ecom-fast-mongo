from fastapi import APIRouter, HTTPException, status
from pydantic import EmailStr
from passlib.context import CryptContext
from mongoengine import ValidationError
from app.models.user import User  # Import your MongoDB User model
from app.schemas.user import UserCreate, UserResponse  # Import your Pydantic schemas
from app.utils.jwt import create_access_token, create_refresh_token  # Import JWT functions
from datetime import datetime


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


router = APIRouter()

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Utility function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Utility function to check if a user already exists by email
def check_user_exists(email: EmailStr) -> bool:
    return User.objects(email=email).first() is not None

@router.post("/api/users", status_code=status.HTTP_201_CREATED)
async def sign_up(user: UserCreate):
    if check_user_exists(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password before saving
    hashed_password = hash_password(user.password)

    try:
        # Create a new user document
        new_user = User(
            name=user.name,
            email=user.email,
            password=hashed_password,
            dob=user.dob,
        )
        # Save the user to the database
        new_user.save()

        # Generate access and refresh tokens
        access_token = create_access_token({"sub": str(new_user.id)})
        refresh_token = create_refresh_token({"sub": str(new_user.id)})

        # Ensure that dates are not None
        created_at = new_user.createdAt.isoformat() if new_user.createdAt else datetime.utcnow().isoformat()
        updated_at = new_user.updatedAt.isoformat() if new_user.updatedAt else datetime.utcnow().isoformat()

        # Return the user response along with tokens
        return {
            "user": UserResponse(
                id=str(new_user.id),  # Access the default MongoDB _id field
                name=new_user.name,
                email=new_user.email,
                dob=new_user.dob,
                createdAt=created_at,
                updatedAt=updated_at,
            ),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MongoDB validation error: " + str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred: " + str(e)
        )
