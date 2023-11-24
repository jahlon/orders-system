from fastapi import FastAPI

from app.routers import products

description = """
Orders System API simulates a simple order management system. 
It allows you to create, update, delete and get orders and products.
It is intended to be used as a sample project for learning design patterns and principles to
design and implement maintainable and reusable software.

## Products
Products are the items that are sold by the system.
You will be able to:
- Create a product
- Update a product
- Delete a product
- Get a product by sku
- Get all products

## Orders
Orders are the main entity of the system.
You will be able to:
- Create an order
- Get an order by id
- Get all orders
"""


tags_metadata = [
    {
        "name": "products",
        "description": "Operations related to products",
    },
    {
        "name": "orders",
        "description": "Operations related to orders",
    },
]

app = FastAPI(
    title="Orders System API",
    description=description,
    version="1.0.0",
    contact={
        "name": "Jesús Andrés Hincapié",
        "email": "jahlon@gmail.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=tags_metadata,
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)


app.include_router(products.router)
