from app.data.errors import UserNotFoundError
from app.data.models import UserInDB
from app.services.interfaces import IUserService


class UserServiceMock(IUserService):
    def __init__(self):
        self.users_collection = [
            {
                "username": 'admin',
                "email": "admin@gmail.com",
                "full_name": "Administrator",
                "disabled": False,
                "hashed_password": '$2b$12$oJiP8xt.pXYyM4YSUI5b/.DivAFiVCXm7xkh15dckrkcRdlYE88J.',
                "scopes": 'order_read order_write product_read product_write me'
            },
            {
                "username": 'user',
                "email": "user@gmail.com",
                "full_name": "User",
                "disabled": False,
                "hashed_password": '$2b$12$uz1e.1hPOKl6XwYzuqgvD.afJXuPKG0/6M5cAE40B504Ea0tciSmm',
                "scopes": 'order_read product_read'
            },
        ]

    def get_by_username(self, username: str) -> UserInDB:
        user = next((user for user in self.users_collection if user['username'] == username), None)
        if not user:
            raise UserNotFoundError(f"User with username {username} not found")
        return UserInDB(**user)
