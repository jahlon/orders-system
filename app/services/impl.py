from typing import Annotated

from fastapi import Depends
from pymongo import ReturnDocument
from pymongo.errors import PyMongoError

from app.data.errors import ProductNotFoundError, ProductAlreadyExistsError, CouldNotUpdateProductError
from app.data.models import Product
from app.data.repository import OrdersSystemRepository
from app.data.schemas import product_schema
from app.services.interfaces import IProductService


class ProductService(IProductService):
    def __init__(self, repository: Annotated[OrdersSystemRepository, Depends(OrdersSystemRepository)]):
        self.product_collection = repository.get_collection('products')

    def get_all(self) -> list[Product]:
        products = list(map(lambda product: product_schema(product), self.product_collection.find()))
        return list(map(lambda product: Product(**product), products))

    def get_by_sku(self, product_sku: str) -> Product:
        product = self.product_collection.find_one({'sku': product_sku})
        if not product:
            raise ProductNotFoundError(f"Product with sku {product_sku} not found")
        return Product(**product_schema(product))

    def create(self, product: Product) -> Product:
        found_product = self.product_collection.find_one({'sku': product.sku})
        if found_product:
            raise ProductAlreadyExistsError(f"Product with sku {product.sku} already exists")

        product_dict = dict(product)
        _id = self.product_collection.insert_one(product_dict).inserted_id
        new_product = product_schema(self.product_collection.find_one({"_id": _id}))
        return Product(**new_product)

    def update(self, product: Product) -> Product:
        product_dict = dict(product)
        sku = product.sku
        try:
            updated_product = self.product_collection.find_one_and_replace({'sku': sku}, product_dict,
                                                                           return_document=ReturnDocument.AFTER)
        except PyMongoError as err:
            raise CouldNotUpdateProductError(f"Could not update product with sku {sku}") from err
        else:
            return Product(**product_schema(updated_product))

    def delete(self, product_sku):
        found = self.product_collection.find_one_and_delete({'sku': product_sku})
        if not found:
            raise ProductNotFoundError(f"Product with sku {product_sku} not found")
