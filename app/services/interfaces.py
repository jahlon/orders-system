from typing import Protocol

from app.data.models import Product


class IProductService(Protocol):
    def get_all(self):
        ...

    def get_by_sku(self, product_sku: str):
        ...

    def create(self, product: Product):
        ...

    def update(self, product: Product):
        ...

    def delete(self, product_id: str):
        ...
