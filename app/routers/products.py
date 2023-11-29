from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form, Security

from app.controllers.product_controller import ProductController
from app.data.errors import ProductNotFoundError, ProductAlreadyExistsError, CouldNotUpdateProductError, \
    CouldNotUploadFileError
from app.data.models import Product, User
from app.services.security import get_current_active_user

router = APIRouter(
    prefix='/products',
    tags=['products'],
    responses={404: {'description': 'Not found'}},
)

ControllerDependency = Annotated[ProductController, Depends(ProductController)]


@router.get('/')
async def get_products(controller: ControllerDependency,
                       current_user: Annotated[
                           User, Security(get_current_active_user, scopes=["product_read"])]) -> list[Product]:
    return controller.get_all()


@router.get('/{product_sku}')
async def get_product(product_sku: str, controller: ControllerDependency,
                      current_user: Annotated[
                          User, Security(get_current_active_user, scopes=["product_read"])]) -> Product:
    try:
        return controller.get_by_sku(product_sku)
    except ProductNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.post('/')
async def create_product(sku: Annotated[str, Form()], name: Annotated[str, Form()],
                         description: Annotated[str, Form()], price: Annotated[float, Form()],
                         image: UploadFile, controller: ControllerDependency,
                         current_user: Annotated[
                             User, Security(get_current_active_user, scopes=["product_write"])]) -> Product:
    try:
        return await controller.create(sku=sku, name=name, description=description, price=price, image=image)
    except ProductAlreadyExistsError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    except CouldNotUploadFileError as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))


@router.put('/')
async def update_product(sku: Annotated[str, Form()], name: Annotated[str, Form()],
                         description: Annotated[str, Form()], price: Annotated[float, Form()],
                         controller: ControllerDependency,
                         current_user: Annotated[
                             User, Security(get_current_active_user, scopes=["product_write"])],
                         image: UploadFile = UploadFile(None)) -> Product:
    try:
        return await controller.update(sku=sku, name=name, description=description, price=price, image=image)
    except ProductNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except CouldNotUpdateProductError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.delete('/{product_sku}')
async def delete_product(product_sku: str, controller: ControllerDependency,
                         current_user: Annotated[
                             User, Security(get_current_active_user, scopes=["product_write"])]) -> Product:
    try:
        return await controller.delete(product_sku)
    except ProductNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
