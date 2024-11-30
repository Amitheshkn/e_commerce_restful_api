from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, title="Product Name")
    description: Optional[str] = Field(None, max_length=500, title="Product Description")
    price: float = Field(..., gt=0, title="Product Price")
    stock: int = Field(..., ge=0, title="Stock Quantity")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Laptop",
                "description": "A high-performance laptop with 16GB RAM and 512GB SSD.",
                "price": 1200.0,
                "stock": 10
            }
        }


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: str = Field(..., title="Product ID")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "64c8f2fce9a123456789001",
                "name": "Laptop",
                "description": "A high-performance laptop with 16GB RAM and 512GB SSD.",
                "price": 1200.0,
                "stock": 10
            }
        }
