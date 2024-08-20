from fastapi import APIRouter, HTTPException, status
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from mongoengine import ValidationError
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/api/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    try:
        # Create a new product document
        new_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
        )
        # Save the product to the database
        new_product.save()

        # Ensure that dates are not None
        created_at = new_product.createdAt.isoformat() if new_product.createdAt else datetime.utcnow().isoformat()
        updated_at = new_product.updatedAt.isoformat() if new_product.updatedAt else datetime.utcnow().isoformat()

        return ProductResponse(
            id=str(new_product.id),  # Access the default MongoDB _id field
            name=new_product.name,
            description=new_product.description,
            price=new_product.price,
            stock=new_product.stock,
            createdAt=created_at,
            updatedAt=updated_at,
        )
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



@router.get("/api/products", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
async def get_all_products():
    try:
        products = Product.objects()  # Retrieve all products
        return [
            ProductResponse(
                id=str(product.id),
                name=product.name,
                description=product.description,
                price=product.price,
                stock=product.stock,
                createdAt=product.createdAt.isoformat() if product.createdAt else None,
                updatedAt=product.updatedAt.isoformat() if product.updatedAt else None
            )
            for product in products
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred: " + str(e)
        )

@router.put("/api/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product: ProductUpdate):
    try:
        existing_product = Product.objects(id=product_id).first()
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        if product.name is not None:
            existing_product.name = product.name
        if product.description is not None:
            existing_product.description = product.description
        if product.price is not None:
            existing_product.price = product.price
        if product.stock is not None:
            existing_product.stock = product.stock
        
        existing_product.save()
        
        return ProductResponse(
            id=str(existing_product.id),
            name=existing_product.name,
            description=existing_product.description,
            price=existing_product.price,
            stock=existing_product.stock,
            createdAt=existing_product.createdAt.isoformat() if existing_product.createdAt else None,
            updatedAt=existing_product.updatedAt.isoformat() if existing_product.updatedAt else None,
        )
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



@router.delete("/api/products/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: str):
    try:
        # Check if the product exists
        existing_product = Product.objects(id=product_id).first()
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        # Delete the product
        result = Product.objects(id=product_id).delete()
        
        if result == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        # Return a success message
        return {"message": "Product deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred: " + str(e)
        )