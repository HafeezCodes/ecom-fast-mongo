from fastapi import APIRouter, HTTPException, status
from mongoengine import ValidationError
from app.models.user import User  
from app.schemas.user import UserCreate, UserResponse , UserSignIn 
from datetime import datetime
from app.utils.jwt import create_access_token, create_refresh_token 
from pydantic import EmailStr
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


# Utility function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Utility function to check if a user already exists by email
def check_user_exists(email: EmailStr) -> bool:
    return User.objects(email=email).first() is not None


# Utility function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Utility function to get user by email
def get_user_by_email(email: EmailStr):
    return User.objects(email=email).first()

router = APIRouter()

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



@router.post("/api/users/sign_in", status_code=status.HTTP_200_OK)
async def sign_in(user: UserSignIn):
    # Fetch user by email
    db_user = get_user_by_email(user.email)
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify the password
    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    #fetch user data from db
    user = UserResponse(
        id=str(db_user.id),
        name=db_user.name,
        email=db_user.email,
        dob=db_user.dob,
        createdAt=db_user.createdAt.isoformat() if db_user.createdAt else datetime.utcnow().isoformat(),
        updatedAt=db_user.updatedAt.isoformat() if db_user.updatedAt else datetime.utcnow().isoformat()
    )
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": str(db_user.id)}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(db_user.id)}
    )
    
    return {
        "user": user,
        "access_token": access_token,
        "refresh_token": refresh_token
    }