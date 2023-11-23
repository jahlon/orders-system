from app.services.interfaces import IProductService


class ProductController:
    def __init__(self, product_service: IProductService):
        self.product_service = product_service

    def get_all(self):
        return self.product_service.get_all()

    def get_by_id(self, product_id):
        return self.product_service.get_by_id(product_id)

    def create(self, product):
        return self.product_service.create(product)

    def update(self, product_id, product):
        return self.product_service.update(product_id, product)

    def delete(self, product_id):
        return self.product_service.delete(product_id)