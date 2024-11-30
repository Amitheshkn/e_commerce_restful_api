from fastapi import APIRouter
from fastapi import status

from e_commerce_app.api.orders.actions import OrderActions
from e_commerce_app.schemas.orders_schema import OrderCreate
from e_commerce_app.schemas.orders_schema import OrderOut

orders_router = APIRouter(prefix="/orders", tags=["Orders"])


@orders_router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderOut)
def create_order(order: OrderCreate):
    return OrderActions.create_order(order)
