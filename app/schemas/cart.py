from pydantic import BaseModel
from typing import Optional
import datetime

class CartItemCreate(BaseModel):
    product_id: str

class CartItemResponse(BaseModel):
    id: str
    user_id: str
    product_id: str
    quantity: int
    createdAt: str
    updatedAt: str

    class Config:
        json_encoders = {
            datetime.datetime: lambda v: v.isoformat(),
            datetime.date: lambda v: v.isoformat()
        }

class CartItemDelete(BaseModel):
    product_id: str
    quantity: int