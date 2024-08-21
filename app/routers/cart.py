from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from bson import ObjectId
from app.models.cart import CartItem
from app.schemas.cart import CartItemCreate, CartItemResponse, CartItemDelete
from app.security import UserAuthenticator, oauth2_scheme


router = APIRouter()
user_authenticator = UserAuthenticator()

@router.post("/api/users/{user_id}/cart", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
async def add_to_cart(user_id: str, cart_item: CartItemCreate, token: str = Depends(oauth2_scheme)):
    user_authenticator.authenticate_user(token, user_id)

    existing_item = CartItem.objects(user_id=ObjectId(user_id), product_id=cart_item.product_id).first()
    if existing_item:
        existing_item.quantity += 1  # Increment quantity by 1
        existing_item.save()  # Save the updated item
        return CartItemResponse(
            id=str(existing_item.id),
            user_id=str(existing_item.user_id.id),
            product_id=str(existing_item.product_id.id),
            quantity=existing_item.quantity,
            createdAt=existing_item.createdAt.isoformat() if existing_item.createdAt else None,
            updatedAt=existing_item.updatedAt.isoformat() if existing_item.updatedAt else None
        )

    new_cart_item = CartItem(
        user_id=ObjectId(user_id),
        product_id=cart_item.product_id,
        quantity=1  # Set quantity to 1 for new items
    )
    new_cart_item.save()  # Save the new cart item

    return CartItemResponse(
        id=str(new_cart_item.id),
        user_id=str(new_cart_item.user_id.id),
        product_id=str(new_cart_item.product_id.id),
        quantity=new_cart_item.quantity,
        createdAt=new_cart_item.createdAt.isoformat() if new_cart_item.createdAt else None,
        updatedAt=new_cart_item.updatedAt.isoformat() if new_cart_item.updatedAt else None
    )




@router.get("/api/users/{user_id}/cart", response_model=List[CartItemResponse])
async def get_cart(user_id: str, token: str = Depends(oauth2_scheme)):
    user_authenticator.authenticate_user(token, user_id)  # Ensure user is authenticated

    cart_items = CartItem.objects(user_id=ObjectId(user_id))

    if not cart_items:
        # Return a custom message when no items are in the cart
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No items in the cart."
        )

    return [CartItemResponse(
        id=str(item.id),
        user_id=str(item.user_id.id),
        product_id=str(item.product_id.id),
        quantity=item.quantity,
        createdAt=item.createdAt.isoformat() if item.createdAt else None,
        updatedAt=item.updatedAt.isoformat() if item.updatedAt else None
    ) for item in cart_items]

@router.delete("/api/users/{user_id}/cart/{cart_item_id}", status_code=status.HTTP_200_OK)
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



@router.patch("/api/users/{user_id}/cart/{product_id}/reduce", status_code=status.HTTP_200_OK)
async def reduce_cart_item_quantity(user_id: str, product_id: str, token: str = Depends(oauth2_scheme)):
    user_authenticator.authenticate_user(token, user_id)  # Ensure user is authenticated
    
    # Find the cart item
    cart_item = CartItem.objects(user_id=ObjectId(user_id), product_id=ObjectId(product_id)).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    # Reduce the quantity by 1
    cart_item.quantity -= 1

    if cart_item.quantity <= 0:
        # If the quantity reaches 0, remove the item from the cart
        cart_item.delete()
        return {"message": "Cart item removed successfully because quantity reached 0"}
    
    # Otherwise, save the updated cart item
    cart_item.save()
    return CartItemResponse(
        id=str(cart_item.id),
        user_id=str(cart_item.user_id.id),
        product_id=str(cart_item.product_id.id),  # Ensure correct access to product_id
        quantity=cart_item.quantity,
        createdAt=cart_item.createdAt.isoformat() if cart_item.createdAt else None,
        updatedAt=cart_item.updatedAt.isoformat() if cart_item.updatedAt else None
    )



