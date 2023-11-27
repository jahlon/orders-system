from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.controllers.order_controller import OrderController
from app.data.errors import OrderNotFoundError
from app.data.models import OrderIn, OrderOut

router = APIRouter(
    prefix='/orders',
    tags=['orders'],
    responses={404: {'description': 'Not found'}},
)

ControllerDependency = Annotated[OrderController, Depends(OrderController)]


@router.get('/')
async def get_orders(controller: ControllerDependency) -> list[OrderOut]:
    return controller.get_all()


@router.get('/{order_id}')
async def get_order(order_id: str, controller: ControllerDependency) -> OrderOut:
    try:
        return controller.get_by_id(order_id)
    except OrderNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.post('/')
async def create_order(order: OrderIn, controller: ControllerDependency) -> OrderOut:
    return await controller.create(order)
