from app.data.repository import OrdersSystemRepository
from app.services.interfaces import IProductService


class ProductService(IProductService):
    def __init__(self, repository: OrdersSystemRepository):
        self.product_collection = repository.get_collection('products')

    def get_all(self):
        return self.product_repository.get_all()

    def get_by_id(self, product_id):
        return self.product_repository.get_by_id(product_id)

    def create(self, product):
        return self.product_repository.create(product)

    def update(self, product_id, product):
        return self.product_repository.update(product_id, product)

    def delete(self, product_id):
        return self.product_repository.delete(product_id)