from typing import Annotated

from bson import ObjectId
from fastapi import Depends
from pymongo import ReturnDocument
from pymongo.errors import PyMongoError

from app.data.errors import ProductNotFoundError, ProductAlreadyExistsError, CouldNotUpdateProductError, \
    OrderNotFoundError, UserNotFoundError
from app.data.models import Product, OrderOut, UserInDB
from app.data.repository import OrdersSystemRepository
from app.services.interfaces import IProductService, IOrderService, IUserService


class ProductService(IProductService):
    def __init__(self, repository: Annotated[OrdersSystemRepository, Depends(OrdersSystemRepository)]):
        self.product_collection = repository.get_collection('products')

    def get_all(self) -> list[Product]:
        products = list(self.product_collection.find())
        return list(map(lambda product: Product(**product), products))

    def get_by_sku(self, product_sku: str) -> Product:
        product = self.product_collection.find_one({'sku': product_sku})
        if not product:
            raise ProductNotFoundError(f"Product with sku {product_sku} not found")
        return Product(**product)

    def create(self, product: Product) -> Product:
        found_product = self.product_collection.find_one({'sku': product.sku})
        if found_product:
            raise ProductAlreadyExistsError(f"Product with sku {product.sku} already exists")

        product_dict = dict(product)
        _id = self.product_collection.insert_one(product_dict).inserted_id
        new_product = self.product_collection.find_one({"_id": _id})
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
            return Product(**updated_product)

    def delete(self, product_sku):
        found = self.product_collection.find_one_and_delete({'sku': product_sku})
        if not found:
            raise ProductNotFoundError(f"Product with sku {product_sku} not found")
        return Product(**found)


class OrderService(IOrderService):
    def __init__(self, repository: Annotated[OrdersSystemRepository, Depends(OrdersSystemRepository)]):
        self.order_collection = repository.get_collection('orders')

    def get_all(self) -> list[OrderOut]:
        orders = list(self.order_collection.find())
        return list(map(lambda order: OrderOut(**order), orders))

    def get_by_id(self, order_id: str) -> OrderOut:
        order = self.order_collection.find_one({'id': order_id})
        if not order:
            raise OrderNotFoundError(f"Order with id {order_id} not found")
        return OrderOut(**order)

    def create(self, order: OrderOut) -> OrderOut:
        order_dict = dict(order.model_dump())
        _id = self.order_collection.insert_one(order_dict).inserted_id
        new_order = self.order_collection.find_one({"_id": ObjectId(_id)})
        return OrderOut(**new_order)


class UserService(IUserService):
    def __init__(self, repository: Annotated[OrdersSystemRepository, Depends(OrdersSystemRepository)]):
        self.users_collection = repository.get_collection('users')

    def get_by_username(self, username: str) -> UserInDB:
        user = self.users_collection.find_one({'username': username})
        if not user:
            raise UserNotFoundError(f"User with username {username} not found")
        return UserInDB(**user)
