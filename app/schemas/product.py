from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int

    class Config:
        schema_extra = {
            "example": {
                "name": "Sample Product",
                "description": "This is a sample product.",
                "price": 29.99,
                "stock": 100
            }
        }

class ProductUpdate(BaseModel):
    # id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

class ProductResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }