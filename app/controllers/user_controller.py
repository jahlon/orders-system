from typing import Annotated

from fastapi import Depends

from app.data.models import UserIn, UserInDB
from app.services.impl import UserService
from app.services.interfaces import IUserService
from app.services.security import get_password_hash

USER_SCOPES = "product_read product_write user_order_read order_write me"


class UserController:
    def __init__(self, user_service: Annotated[IUserService, Depends(UserService)]):
        self.user_service = user_service

    def get_by_username(self, username: str):
        return self.user_service.get_by_username(username)

    def register_user(self, user: UserIn):
        hashed_password = get_password_hash(user.password)
        data = dict(user)
        data['hashed_password'] = hashed_password
        data['scopes'] = USER_SCOPES
        return self.user_service.create(UserInDB(**data))
