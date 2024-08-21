from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from bson import ObjectId
from app.models.cart import CartItem
from app.schemas.cart import CartItemCreate, CartItemResponse
from app.security import UserAuthenticator, oauth2_scheme
from app.utils.formatting import cart_mongo_to_pydantic

router = APIRouter()
user_authenticator = UserAuthenticator()

# Add to cart (+1)
@router.post("/api/users/{user_id}/cart", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
async def add_to_cart(user_id: str, cart_item: CartItemCreate, token: str = Depends(oauth2_scheme)):
    user_authenticator.authenticate_user(token, user_id)

    existing_item = CartItem.objects(user_id=ObjectId(user_id), product_id=cart_item.product_id).first()
    if existing_item:
        existing_item.quantity += 1
        existing_item.save()
        return cart_mongo_to_pydantic(existing_item, CartItemResponse)

    new_cart_item = CartItem(
        user_id=ObjectId(user_id),
        product_id=cart_item.product_id,
        quantity=1
    )
    new_cart_item.save()
    return cart_mongo_to_pydantic(new_cart_item, CartItemResponse)


# Get all cart items
@router.get("/api/users/{user_id}/cart", response_model=List[CartItemResponse])
async def get_cart(user_id: str, token: str = Depends(oauth2_scheme)):
    user_authenticator.authenticate_user(token, user_id)

    cart_items = CartItem.objects(user_id=ObjectId(user_id))
    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No items in the cart."
        )

    return [cart_mongo_to_pydantic(item, CartItemResponse) for item in cart_items]

# Remove whole item from cart
@router.delete("/api/users/{user_id}/cart/{cart_item_id}", status_code=status.HTTP_200_OK)
async def remove_from_cart(user_id: str, cart_item_id: str, token: str = Depends(oauth2_scheme)):
    user_authenticator.authenticate_user(token, user_id)

    cart_item = CartItem.objects(id=ObjectId(cart_item_id), user_id=ObjectId(user_id)).first()
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )

    cart_item.delete()
    return {"message": "Cart item removed successfully"}


# Reduce quantity of cart item (-1) and remove whole item if quantity reaches 0
@router.patch("/api/users/{user_id}/cart/{product_id}/reduce", status_code=status.HTTP_200_OK)
async def reduce_cart_item_quantity(user_id: str, product_id: str, token: str = Depends(oauth2_scheme)):
    user_authenticator.authenticate_user(token, user_id)

    cart_item = CartItem.objects(user_id=ObjectId(user_id), product_id=ObjectId(product_id)).first()
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )

    cart_item.quantity -= 1
    if cart_item.quantity <= 0:
        cart_item.delete()
        return {"message": "Cart item removed successfully because quantity reached 0"}

    cart_item.save()
    return cart_mongo_to_pydantic(cart_item, CartItemResponse)
