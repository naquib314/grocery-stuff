from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ProductBase(BaseModel):
    product_id: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=50)
    unit: str = Field(..., min_length=1, max_length=20)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    unit: Optional[str] = Field(None, min_length=1, max_length=20)


class Product(ProductBase):
    id: int
    store_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    store: Optional["Store"] = None
    
    class Config:
        from_attributes = True


class StoreBase(BaseModel):
    store_id: str = Field(..., min_length=1, max_length=50)
    store_name: str = Field(..., min_length=1, max_length=100)
    location: Optional[str] = Field(None, max_length=200)


class StoreCreate(StoreBase):
    pass


class StoreUpdate(BaseModel):
    store_name: Optional[str] = Field(None, min_length=1, max_length=100)
    location: Optional[str] = Field(None, max_length=200)


class Store(StoreBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class StoreWithProducts(Store):
    products: List[Product] = []


class ProductSearchResponse(BaseModel):
    query: str
    results: List[Product]
    total_results: int


class PriceComparisonResponse(BaseModel):
    product_name: str
    products: List[Product]
    cheapest_store: Optional[str] = None
    price_difference: Optional[float] = None
