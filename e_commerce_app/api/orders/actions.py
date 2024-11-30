from bson import ObjectId
from fastapi import HTTPException
from fastapi import status

from e_commerce_app.db.definitions import Collection
from e_commerce_app.db.mongo_adapters import MongoAdapter
from e_commerce_app.schemas.orders_schema import OrderCreate
from e_commerce_app.schemas.orders_schema import OrderOut
from e_commerce_app.schemas.orders_schema import OrderStatus


class OrderActions:
    @staticmethod
    def create_order(order: OrderCreate,
                     /) -> OrderOut:
        order_data = order.dict()
        products = order_data["products"]
        total_price = 0.0

        for product in products:
            product_id = product["product_id"]
            quantity = product["quantity"]

            product = MongoAdapter(Collection.PRODUCTS).find_document({
                "_id": ObjectId(product_id)
            })
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with ID '{product_id}' not found"
                )

            if product["stock"] < quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for product '{product['name']}'."
                           f" Requested: {quantity}, Available: {product['stock']}"
                )

            total_price += product["price"] * quantity

        for product_in_order in products:
            product_id = product_in_order["product_id"]
            quantity = product_in_order["quantity"]
            MongoAdapter(Collection.PRODUCTS).update_document(
                {
                    "_id": ObjectId(product_id)
                },
                {
                    "$inc": {
                        "stock": -quantity
                    }
                })

        order_data["total_price"] = total_price
        order_data["status"] = OrderStatus.COMPLETED
        order_id = MongoAdapter(Collection.ORDERS).insert_document(order_data)

        return OrderOut(id=order_id, **order_data)
