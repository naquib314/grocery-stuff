from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product: schemas.ProductCreate,
    store_id: int,
    db: Session = Depends(get_db)
):
    """Create a new product for a store"""
    # Verify store exists
    db_store = crud.get_store(db, store_id=store_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    
    return crud.create_product(db=db, product=product, store_id=store_id)


@router.get("/", response_model=List[schemas.Product])
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all products"""
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


@router.get("/search", response_model=schemas.ProductSearchResponse)
def search_products(
    q: str = Query(..., min_length=1, description="Search query for product name or category"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Search for products by name or category"""
    products = crud.search_products(db, query=q, skip=skip, limit=limit)
    return schemas.ProductSearchResponse(
        query=q,
        results=products,
        total_results=len(products)
    )


@router.get("/compare", response_model=schemas.PriceComparisonResponse)
def compare_product_prices(
    product_name: str = Query(..., min_length=1, description="Product name to compare prices"),
    db: Session = Depends(get_db)
):
    """Compare prices of a product across all stores"""
    products = crud.get_product_price_comparison(db, product_name=product_name)
    
    if not products:
        raise HTTPException(
            status_code=404, 
            detail=f"No products found matching '{product_name}'"
        )
    
    # Find the cheapest option
    cheapest_product = min(products, key=lambda p: p.price)
    most_expensive_product = max(products, key=lambda p: p.price)
    price_difference = most_expensive_product.price - cheapest_product.price
    
    return schemas.PriceComparisonResponse(
        product_name=product_name,
        products=products,
        cheapest_store=cheapest_product.store.store_name,
        price_difference=price_difference
    )


@router.get("/{product_id}", response_model=schemas.Product)
def read_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific product"""
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.put("/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int,
    product_update: schemas.ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update a product"""
    db_product = crud.update_product(db, product_id=product_id, product_update=product_update)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Delete a product"""
    success = crud.delete_product(db, product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
