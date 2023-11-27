from typing import Protocol

from app.data.models import Product, OrderOut, OrderIn


class IProductService(Protocol):
    def get_all(self) -> list[Product]:
        ...

    def get_by_sku(self, product_sku: str) -> Product:
        ...

    def create(self, product: Product) -> Product:
        ...

    def update(self, product: Product) -> Product:
        ...

    def delete(self, product_id: str):
        ...


class IOrderService(Protocol):
    def get_all(self) -> list[OrderOut]:
        ...

    def get_by_id(self, order_id: str) -> OrderOut:
        ...

    def create(self, order: OrderOut) -> OrderOut:
        ...
