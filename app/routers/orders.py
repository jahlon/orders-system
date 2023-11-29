from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security
from starlette import status

from app.controllers.order_controller import OrderController
from app.data.errors import OrderNotFoundError
from app.data.models import OrderIn, OrderOut, User
from app.services.security import get_current_active_user

router = APIRouter(
    prefix='/orders',
    tags=['orders'],
    responses={
        404: {
            'description': 'Not found'
        },
        401: {
            'description': 'Unauthorized',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Not enough permissions',
                    }
                }
            }
        }
    },
)

ControllerDependency = Annotated[OrderController, Depends(OrderController)]


@router.get('/', dependencies=[Security(get_current_active_user, scopes=["order_read"])])
async def get_orders(controller: ControllerDependency) -> list[OrderOut]:
    return controller.get_all()


@router.get('/{order_id}', dependencies=[Security(get_current_active_user, scopes=["order_read"])])
async def get_order(order_id: str, controller: ControllerDependency) -> OrderOut:
    try:
        return controller.get_by_id(order_id)
    except OrderNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.post('/', dependencies=[Security(get_current_active_user, scopes=["order_write"])])
async def create_order(order: OrderIn, controller: ControllerDependency) -> OrderOut:
    return await controller.create(order)
