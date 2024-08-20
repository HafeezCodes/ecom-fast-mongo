from pydantic import BaseModel, EmailStr
from datetime import date
import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    dob: date

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "password": "password123",
                "dob": "1990-01-01"
            }
        }

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    dob: date
    createdAt: str
    updatedAt: str

    class Config:
        json_encoders = {
            datetime.datetime: lambda v: v.isoformat(),
            datetime.date: lambda v: v.isoformat()
        }
