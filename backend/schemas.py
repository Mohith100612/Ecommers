from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class ProductBase(BaseModel):
    product_id: str
    title: str
    category: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = 0.0
    rating: Optional[float] = 0.0
    review_count: Optional[int] = 0
    description: Optional[str] = None
    features: List[str] = []
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    image_url: Optional[str] = None

class Product(ProductBase):
    id: int
    image_description: Optional[str] = None

    class Config:
        from_attributes = True

class SearchResult(BaseModel):
    product: Product
    score: float

class SearchResponse(BaseModel):
    results: List[SearchResult]
    answer: str
