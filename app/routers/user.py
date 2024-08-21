from fastapi import APIRouter, HTTPException, status
from app.models.user import User, hash_password, check_user_exists, verify_password, get_user_by_email
from app.schemas.user import UserCreate, UserResponse, UserSignIn
from app.utils.jwt import create_access_token, create_refresh_token
from datetime import datetime
from app.utils.formatting import format_mongo_to_pydantic

router = APIRouter()

@router.post("/api/users", status_code=status.HTTP_201_CREATED)
async def sign_up(user: UserCreate):
    if check_user_exists(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        dob=user.dob,
    )

    new_user.save()

    access_token = create_access_token({"sub": str(new_user.id)})
    refresh_token = create_refresh_token({"sub": str(new_user.id)})

     # Format the user response
    user_response = format_mongo_to_pydantic(new_user, UserResponse)

    # Return the custom response
    return {
        "user": user_response,
        "access_token": access_token,
        "refresh_token": refresh_token
    }

    return {
        "user": UserResponse(
            id=str(new_user.id),  
            name=new_user.name,
            email=new_user.email,
            dob=new_user.dob,
            createdAt=str(new_user.createdAt),
            updatedAt=str(new_user.updatedAt),
        ),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

    

@router.post("/api/users/sign_in", status_code=status.HTTP_200_OK)
async def sign_in(user: UserSignIn):
    db_user = get_user_by_email(user.email)
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(data={"sub": str(db_user.id)})
    refresh_token = create_refresh_token(data={"sub": str(db_user.id)})
    
     # Format the user response
    user_response = format_mongo_to_pydantic(db_user, UserResponse)

    # Return the custom response
    return {
        "user": user_response,
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    

    return {
        "user": user_response,
        "access_token": access_token,
        "refresh_token": refresh_token
    }
