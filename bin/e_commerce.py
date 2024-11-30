from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from e_commerce_app.api.orders.routes import orders_router
from e_commerce_app.api.products.routes import products_router

app = FastAPI(title="E-Commerce API",
              description="e-commerce platform")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Router files
app.include_router(orders_router)
app.include_router(products_router)
