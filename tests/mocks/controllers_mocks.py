from typing import Annotated

from fastapi import Depends, UploadFile

from app.data.errors import CouldNotUploadFileError
from app.data.models import Product, UserInDB
from app.services.impl import ProductService, UserService
from app.services.interfaces import IProductService, IUserService
from app.services.security import get_password_hash


class ProductControllerMock:
    def __init__(self, product_service: Annotated[IProductService, Depends(ProductService)]):
        self.product_service = product_service

    async def create(self, sku: str, name: str, description: str, price: float, image: UploadFile):
        if image.filename == "bad_image.png":
            raise CouldNotUploadFileError("Could not upload file")

        extension = image.filename.split('.')[-1]
        image_name = f"{sku}.{extension}"
        image_url = f"https://example.com/{image_name}"
        product = Product(sku=sku, name=name, description=description, price=price, image_url=image_url)
        return self.product_service.create(product)

    async def update(self, sku: str, name: str, description: str, price: float, image: UploadFile | None):
        if image and image.filename == "bad_image.png":
            raise CouldNotUploadFileError("Could not upload file")

        stored_product = self.product_service.get_by_sku(sku)

        update_data = {
            'name': name,
            'description': description,
            'price': price
        }

        if image and image.file:
            extension = image.filename.split('.')[-1]
            image_name = f"{sku}.{extension}"
            image_url = f"https://example.com/{image_name}"
            update_data['image_url'] = image_url

        updated_product = stored_product.model_copy(update=update_data)
        return self.product_service.update(updated_product)

    async def delete(self, product_sku):
        return self.product_service.delete(product_sku)
