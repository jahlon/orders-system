from typing import Protocol


class IProductService(Protocol):
    def get_all(self):
        ...

    def get_by_id(self, product_id):
        ...

    def create(self, product):
        ...

    def update(self, product_id, product):
        ...

    def delete(self, product_id):
        ...
