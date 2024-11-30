from enum import Enum


class Database:
    E_COMMERCE = "e_commerce"


class Collection(str, Enum):
    ORDERS = "orders"
    PRODUCTS = "products"
