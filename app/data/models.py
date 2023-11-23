from pydantic import BaseModel


class Product(BaseModel):
    sku: str
    name: str
    description: str
    price: float
    image: str


class Order(BaseModel):
    id: str
    products: list[Product]
    total: float
    status: str
    created_at: str
    updated_at: str
