from typing import Annotated

from fastapi import Depends, UploadFile

from app.data.models import Product
from app.services.aws_service import upload_file_to_s3
from app.services.impl import ProductService
from app.services.interfaces import IProductService


class ProductController:
    def __init__(self, product_service: Annotated[IProductService, Depends(ProductService)]):
        self.product_service = product_service

    def get_all(self):
        return self.product_service.get_all()

    def get_by_sku(self, product_sku):
        return self.product_service.get_by_sku(product_sku)

    async def create(self, sku: str, name: str, description: str, price: float, image: UploadFile):
        extension = image.filename.split('.')[-1]
        image_name = f"{sku}.{extension}"
        image_url = await upload_file_to_s3(image_name, image.file)
        product = Product(sku=sku, name=name, description=description, price=price, image_url=image_url)
        return self.product_service.create(product)

    async def update(self, sku: str, name: str, description: str, price: float, image: UploadFile | None):

        stored_product = self.product_service.get_by_sku(sku)

        update_data = {
            'name': name,
            'description': description,
            'price': price
        }

        if image.file:
            extension = image.filename.split('.')[-1]
            image_name = f"{sku}.{extension}"
            image_url = await upload_file_to_s3(image_name, image.file)
            update_data['image_url'] = image_url

        updated_product = stored_product.model_copy(update=update_data)
        return self.product_service.update(updated_product)

    def delete(self, product_sku):
        return self.product_service.delete(product_sku)