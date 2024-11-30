from enum import Enum
from typing import List

from pydantic import BaseModel
from pydantic import Field


class ProductInOrder(BaseModel):
    product_id: str = Field(..., title="Product ID")
    quantity: int = Field(..., ge=1, title="Quantity of the product")

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "64c8f2fce9a123456789001",
                "quantity": 2,
            }
        }


class OrderBase(BaseModel):
    products: List[ProductInOrder] = Field(..., title="List of products in the order")

    class Config:
        json_schema_extra = {
            "example": {
                "products": [
                    {
                        "product_id": "64c8f2fce9a123456789001",
                        "quantity": 2
                    },
                    {
                        "product_id": "64c8f2fce9a123456789002",
                        "quantity": 1
                    },
                ]
            }
        }


class OrderCreate(OrderBase):
    pass


class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class OrderOut(OrderBase):
    id: str = Field(..., title="Order ID")
    total_price: float = Field(..., ge=0, title="Total price of the order")
    status: OrderStatus = Field(..., title="Order status", description="Order status (pending, completed, failed)")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "64c8f2fce9a123456789003",
                "products": [
                    {
                        "product_id": "64c8f2fce9a123456789001",
                        "quantity": 2
                    },
                    {
                        "product_id": "64c8f2fce9a123456789002",
                        "quantity": 1
                    },
                ],
                "total_price": 150.0,
                "status": "completed",
            }
        }
