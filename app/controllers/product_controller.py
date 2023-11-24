from typing import Annotated

from fastapi import Depends

from app.services.impl import ProductService
from app.services.interfaces import IProductService


class ProductController:
    def __init__(self, product_service: Annotated[IProductService, Depends(ProductService)]):
        self.product_service = product_service

    def get_all(self):
        return self.product_service.get_all()

    def get_by_sku(self, product_sku):
        return self.product_service.get_by_sku(product_sku)

    def create(self, product):
        return self.product_service.create(product)

    def update(self, product):
        return self.product_service.update(product)

    def delete(self, product_sku):
        return self.product_service.delete(product_sku)