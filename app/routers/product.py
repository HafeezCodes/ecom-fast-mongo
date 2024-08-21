from fastapi import APIRouter, HTTPException, status
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from typing import List
from app.utils.formatting import format_mongo_to_pydantic


router = APIRouter()

@router.post("/api/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):

    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
    )

    new_product.save()
    
    return format_mongo_to_pydantic(new_product, ProductResponse)


@router.get("/api/products", response_model=List[ProductResponse], status_code=status.HTTP_200_OK)
async def get_all_products():

    products = Product.objects()
    
    return [format_mongo_to_pydantic(product, ProductResponse) for product in products]


@router.put("/api/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product: ProductUpdate):

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
    
    return format_mongo_to_pydantic(existing_product, ProductResponse)


@router.delete("/api/products/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: str):

    existing_product = Product.objects(id=product_id).first()
    
    if not existing_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    result = Product.objects(id=product_id).delete()
    
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return {"message": "Product deleted successfully"}
