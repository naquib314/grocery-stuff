from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from . import models, schemas


# Store CRUD operations
def get_store(db: Session, store_id: int) -> Optional[models.Store]:
    return db.query(models.Store).filter(models.Store.id == store_id).first()


def get_store_by_store_id(db: Session, store_id: str) -> Optional[models.Store]:
    return db.query(models.Store).filter(models.Store.store_id == store_id).first()


def get_stores(db: Session, skip: int = 0, limit: int = 100) -> List[models.Store]:
    return db.query(models.Store).offset(skip).limit(limit).all()


def create_store(db: Session, store: schemas.StoreCreate) -> models.Store:
    db_store = models.Store(**store.model_dump())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store


def update_store(db: Session, store_id: int, store_update: schemas.StoreUpdate) -> Optional[models.Store]:
    db_store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if db_store:
        update_data = store_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_store, field, value)
        db.commit()
        db.refresh(db_store)
    return db_store


def delete_store(db: Session, store_id: int) -> bool:
    db_store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if db_store:
        db.delete(db_store)
        db.commit()
        return True
    return False


# Product CRUD operations
def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    return db.query(models.Product).options(joinedload(models.Product.store)).filter(models.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[models.Product]:
    return db.query(models.Product).options(joinedload(models.Product.store)).offset(skip).limit(limit).all()


def get_products_by_store(db: Session, store_id: int, skip: int = 0, limit: int = 100) -> List[models.Product]:
    return db.query(models.Product).options(joinedload(models.Product.store)).filter(models.Product.store_id == store_id).offset(skip).limit(limit).all()


def search_products(db: Session, query: str, skip: int = 0, limit: int = 100) -> List[models.Product]:
    return db.query(models.Product).options(joinedload(models.Product.store)).filter(
        or_(
            models.Product.name.ilike(f"%{query}%"),
            models.Product.category.ilike(f"%{query}%")
        )
    ).offset(skip).limit(limit).all()


def get_product_price_comparison(db: Session, product_name: str) -> List[models.Product]:
    """Get the same product from all stores for price comparison"""
    return db.query(models.Product).options(joinedload(models.Product.store)).filter(
        models.Product.name.ilike(f"%{product_name}%")
    ).all()


def create_product(db: Session, product: schemas.ProductCreate, store_id: int) -> models.Product:
    db_product = models.Product(**product.model_dump(), store_id=store_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product_update: schemas.ProductUpdate) -> Optional[models.Product]:
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        update_data = product_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False
