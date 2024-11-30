from fastapi import HTTPException
from fastapi import status

from e_commerce_app.db.definitions import Collection
from e_commerce_app.db.mongo_adapters import MongoAdapter
from e_commerce_app.schemas.products_schema import ProductCreate
from e_commerce_app.schemas.products_schema import ProductOut


class ProductActions:

    @staticmethod
    def get_all_products() -> list[ProductOut]:
        products = MongoAdapter(Collection.PRODUCTS).find_documents({})
        return [ProductOut(**product) for product in products]

    @staticmethod
    def create_product(product: ProductCreate,
                       /) -> ProductOut:
        product_data = product.dict()
        product_name = product_data["name"]
        product_exists = MongoAdapter(Collection.PRODUCTS).find_document({
            "name": product_name
        })
        if product_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with name '{product_name}' already exists"
            )

        product_id = MongoAdapter(Collection.PRODUCTS).insert_document(product_data)
        return ProductOut(id=product_id, **product_data)
