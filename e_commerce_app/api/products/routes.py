from fastapi import APIRouter
from fastapi import status

from e_commerce_app.api.products.actions import ProductActions
from e_commerce_app.schemas.products_schema import ProductCreate
from e_commerce_app.schemas.products_schema import ProductOut

products_router = APIRouter(prefix="/products", tags=["Products"])


@products_router.get("/", status_code=status.HTTP_200_OK, response_model=list[ProductOut])
def get_products():
    return ProductActions.get_all_products()


@products_router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductOut)
def create_product(product: ProductCreate):
    return ProductActions.create_product(product)
