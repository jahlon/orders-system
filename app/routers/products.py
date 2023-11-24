from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.controllers.product_controller import ProductController
from app.data.errors import ProductNotFoundError, ProductAlreadyExistsError, CouldNotUpdateProductError
from app.data.models import Product

router = APIRouter(
    prefix='/products',
    tags=['products'],
    responses={404: {'description': 'Not found'}},
)

ControllerDependency = Annotated[ProductController, Depends(ProductController)]


@router.get('/')
async def get_products(controller: ControllerDependency) -> list[Product]:
    return controller.get_all()


@router.get('/{product_sku}')
async def get_product(product_sku: str, controller: ControllerDependency) -> Product:
    try:
        return controller.get_by_sku(product_sku)
    except ProductNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.post('/')
async def create_product(product: Product, controller: ControllerDependency) -> Product:
    try:
        return controller.create(product)
    except ProductAlreadyExistsError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.put('/{product_sku}')
async def update_product(product: Product, controller: ControllerDependency) -> Product:
    try:
        return controller.update(product)
    except CouldNotUpdateProductError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))