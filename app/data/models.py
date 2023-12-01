from datetime import datetime
from enum import Enum
from typing import List
from uuid import uuid4

from pydantic import BaseModel, Field


class Product(BaseModel):
    sku: str
    name: str
    description: str
    price: float
    image_url: str


class Item(BaseModel):
    sku: str
    price: float
    quantity: int

    @property
    def total(self) -> float:
        return self.price * self.quantity


class OrderStatus(Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


class OrderBase(BaseModel):
    products: List[Item]
    status: OrderStatus = OrderStatus.PENDING

    class Config:
        use_enum_values = True


class OrderIn(OrderBase):

    model_config = {
        'use_enum_values': True,
        'json_schema_extra': {
            'example': {
                'products': [
                    {
                        'sku': 'SP001',
                        'price': 2,
                        'quantity': 3
                    },
                    {
                        'sku': 'EA001',
                        'price': 850,
                        'quantity': 2
                    }
                ],
                'status': 'pending'
            }
        }
    }


class OrderOut(OrderBase):
    id: str = Field(default_factory=lambda: uuid4().hex)
    total: float | None = None
    user: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def update_total(self):
        self.total = sum(map(lambda item: item.total, self.products))


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = False


class UserIn(User):
    password: str


class UserInDB(User):
    hashed_password: str
    scopes: str
