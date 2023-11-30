from app.data.errors import UserNotFoundError, ProductNotFoundError, ProductAlreadyExistsError, \
    CouldNotUpdateProductError
from app.data.models import UserInDB, Product
from app.services.interfaces import IUserService, IProductService


class ProductServiceMock(IProductService):
    def __init__(self):
        self.products_collection = [
            {
                "sku": "123",
                "name": "Product 123",
                "description": "Description 123",
                "price": 123.0,
                "image_url": "https://example.com/123.png"
            },
            {
                "sku": "456",
                "name": "Product 456",
                "description": "Description 456",
                "price": 456.0,
                "image_url": "https://example.com/456.png"
            },
        ]

    def get_all(self) -> list[Product]:
        return list(map(lambda product: Product(**product), self.products_collection))

    def get_by_sku(self, product_sku: str) -> Product:
        product = next((product for product in self.products_collection if product['sku'] == product_sku), None)
        if not product:
            raise ProductNotFoundError(f"Product with sku {product_sku} not found")
        return Product(**product)

    def create(self, product: Product) -> Product:
        found_product = next((p for p in self.products_collection if p['sku'] == product.sku), None)
        if found_product:
            raise ProductAlreadyExistsError(f"Product with sku {product.sku} already exists")
        self.products_collection.append(dict(product))
        return product

    def update(self, product: Product) -> Product:
        product_dict = dict(product)
        sku = product.sku
        found_product = next((p for p in self.products_collection if p['sku'] == sku), None)
        if not found_product:
            raise CouldNotUpdateProductError(f"Could not update product with sku {sku}")
        self.products_collection = list(map(lambda p: product_dict if p['sku'] == sku else p, self.products_collection))
        return product

    def delete(self, product_sku):
        found_product = next((p for p in self.products_collection if p['sku'] == product_sku), None)
        if not found_product:
            raise ProductNotFoundError(f"Product with sku {product_sku} not found")
        self.products_collection = list(filter(lambda p: p['sku'] != product_sku, self.products_collection))
        return Product(**found_product)


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
