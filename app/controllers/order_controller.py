from typing import Annotated

from fastapi import Depends

from app.data.models import OrderIn, OrderOut
from app.services.impl import OrderService
from app.services.interfaces import IOrderService


class OrderController:
    def __init__(self, order_service: Annotated[IOrderService, Depends(OrderService)]):
        self.order_service = order_service

    def get_all(self):
        return self.order_service.get_all()

    def get_all_by_user(self, username: str):
        return self.order_service.get_all_by_user(username)

    def get_by_id(self, order_id):
        return self.order_service.get_by_id(order_id)

    async def create(self, order: OrderIn, username: str):
        order_to_save = OrderOut(**order.model_dump())
        order_to_save.user = username
        order_to_save.update_total()
        return self.order_service.create(order_to_save)
