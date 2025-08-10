from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/stores",
    tags=["stores"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.Store, status_code=status.HTTP_201_CREATED)
def create_store(
    store: schemas.StoreCreate,
    db: Session = Depends(get_db)
):
    """Create a new store"""
    db_store = crud.get_store_by_store_id(db, store_id=store.store_id)
    if db_store:
        raise HTTPException(
            status_code=400,
            detail="Store with this store_id already registered"
        )
    return crud.create_store(db=db, store=store)


@router.get("/", response_model=List[schemas.Store])
def read_stores(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all stores"""
    stores = crud.get_stores(db, skip=skip, limit=limit)
    return stores


@router.get("/{store_id}", response_model=schemas.StoreWithProducts)
def read_store(
    store_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific store with its products"""
    db_store = crud.get_store(db, store_id=store_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    return db_store


@router.put("/{store_id}", response_model=schemas.Store)
def update_store(
    store_id: int,
    store_update: schemas.StoreUpdate,
    db: Session = Depends(get_db)
):
    """Update a store"""
    db_store = crud.update_store(db, store_id=store_id, store_update=store_update)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    return db_store


@router.delete("/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_store(
    store_id: int,
    db: Session = Depends(get_db)
):
    """Delete a store"""
    success = crud.delete_store(db, store_id=store_id)
    if not success:
        raise HTTPException(status_code=404, detail="Store not found")


@router.get("/{store_id}/products", response_model=List[schemas.Product])
def read_store_products(
    store_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all products for a specific store"""
    db_store = crud.get_store(db, store_id=store_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    
    products = crud.get_products_by_store(db, store_id=store_id, skip=skip, limit=limit)
    return products
