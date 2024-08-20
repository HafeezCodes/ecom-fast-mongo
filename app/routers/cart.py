from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from bson import ObjectId
from app.models.cart import CartItem
from app.schemas.cart import CartItemCreate, CartItemResponse, CartItemDelete
from app.security import UserAuthenticator, oauth2_scheme


router = APIRouter()
user_authenticator = UserAuthenticator()

import logging

@router.post("/api/users/{user_id}/cart", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
async def add_to_cart(user_id: str, cart_item: CartItemCreate, token: str = Depends(oauth2_scheme)):
    user_authenticator.authenticate_user(token, user_id)

    existing_item = CartItem.objects(user_id=ObjectId(user_id), product_id=cart_item.product_id).first()
    if existing_item:
        existing_item.quantity += cart_item.quantity
        logging.info(f"Before save - updatedAt: {existing_item.updatedAt}")
        existing_item.save()  # This should trigger an update for updatedAt
        logging.info(f"After save - updatedAt: {existing_item.updatedAt}")
        return CartItemResponse(
            id=str(existing_item.id),
            user_id=str(existing_item.user_id.id),
            product_id=str(existing_item.product_id),
            quantity=existing_item.quantity,
            createdAt=existing_item.createdAt.isoformat() if existing_item.createdAt else None,
            updatedAt=existing_item.updatedAt.isoformat() if existing_item.updatedAt else None
        )

    new_cart_item = CartItem(
        user_id=ObjectId(user_id),
        product_id=cart_item.product_id,
        quantity=cart_item.quantity
    )
    logging.info(f"Before save new item - createdAt: {new_cart_item.createdAt}, updatedAt: {new_cart_item.updatedAt}")
    new_cart_item.save()  # This should set createdAt and updatedAt
    logging.info(f"After save new item - createdAt: {new_cart_item.createdAt}, updatedAt: {new_cart_item.updatedAt}")

    return CartItemResponse(
        id=str(new_cart_item.id),
        user_id=str(new_cart_item.user_id.id),
        product_id=str(new_cart_item.product_id),
        quantity=new_cart_item.quantity,
        createdAt=new_cart_item.createdAt.isoformat() if new_cart_item.createdAt else None,
        updatedAt=new_cart_item.updatedAt.isoformat() if new_cart_item.updatedAt else None
    )



@router.get("/api/users/{user_id}/cart", response_model=List[CartItemResponse])
async def get_cart(user_id: str, token: str = Depends(oauth2_scheme)):
    user_authenticator.authenticate_user(token, user_id)  # Ensure user is authenticated

    cart_items = CartItem.objects(user_id=ObjectId(user_id))

    return [CartItemResponse(
        id=str(item.id),
        user_id=str(item.user_id.id),
        product_id=str(item.product_id),
        quantity=item.quantity,
        createdAt=item.createdAt.isoformat() if item.createdAt else None,
        updatedAt=item.updatedAt.isoformat() if item.updatedAt else None
    ) for item in cart_items]

@router.delete("/api/users/{user_id}/cart/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart(user_id: str, cart_item_id: str, token: str = Depends(oauth2_scheme)):
    current_user = user_authenticator.authenticate_user(token, user_id)
    
    cart_item = CartItem.objects(id=ObjectId(cart_item_id), user_id=ObjectId(user_id)).first()
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    cart_item.delete()
    return {"message": "Cart item removed successfully"}


@router.delete("/api/users/{user_id}/cart/product", status_code=status.HTTP_204_NO_CONTENT)
async def remove_items_from_cart(user_id: str, cart_item_delete: CartItemDelete, token: str = Depends(oauth2_scheme)):
    # Authenticate user
    user_authenticator.authenticate_user(token, user_id)
    
    # Debug: Print values
    print(f"User ID (string): {user_id}")
    print(f"Product ID (string): {cart_item_delete.product_id}")
    
    # Convert IDs to ObjectId
    try:
        user_id_obj = ObjectId(user_id)
        product_id_obj = ObjectId(cart_item_delete.product_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid ID format: {e}")
    
    # Debug: Print converted ObjectIds
    print(f"User ID (ObjectId): {user_id_obj}")
    print(f"Product ID (ObjectId): {product_id_obj}")
    
    # Find the cart item
    cart_item = CartItem.objects(user_id=user_id_obj, product_id=product_id_obj).first()
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found for the specified product"
        )

    # Check if there are enough items to remove
    if cart_item.quantity < cart_item_delete.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough items to remove"
        )
    
    # Remove or update the quantity of items
    cart_item.quantity -= cart_item_delete.quantity
    if cart_item.quantity == 0:
        cart_item.delete()
    else:
        cart_item.save()
    
    return {"message": "Specified quantity of items removed successfully"}


