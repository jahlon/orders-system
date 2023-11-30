from importlib.resources import files
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.controllers.product_controller import ProductController
from app.data.models import User
from app.main import app
from app.services.impl import ProductService
from app.services.security import get_current_user
from tests.mocks.controllers_mocks import ProductControllerMock
from tests.mocks.services_mocks import ProductServiceMock

client = TestClient(app)


def get_current_user_mock():
    return User(username='admin', email="admin@gmail.com", full_name="Administrator", disabled=False)


def assert_200_response(response):
    assert response.status_code == 200
    assert response.json().get('sku') == "123"
    assert response.json().get('name') == "Product 123"
    assert response.json().get('description') == "Description 123"
    assert response.json().get('price') == 123.0
    assert response.json().get('image_url') == "https://example.com/123.png"


@pytest.fixture
def product_route_dependencies_mock():
    # noinspection PyUnresolvedReferences
    app.dependency_overrides[ProductService] = ProductServiceMock
    # noinspection PyUnresolvedReferences
    app.dependency_overrides[get_current_user] = get_current_user_mock


@pytest.fixture
def product_image():
    path = files("tests").joinpath(Path("fixtures/product_image.png"))
    # noinspection PyTypeChecker
    return open(path, "rb")


def test_get_all_products_return_200_status(product_route_dependencies_mock):
    response = client.get('/products')
    assert response.status_code == 200
    assert len(response.json()) == 2
    app.dependency_overrides = {}


def test_get_product_return_200_status(product_route_dependencies_mock):
    response = client.get('/products/123')
    assert_200_response(response)
    app.dependency_overrides = {}


def test_get_product_return_404_status_with_incorrect_sku(product_route_dependencies_mock):
    response = client.get('/products/incorrect_sku')
    assert response.status_code == 404
    assert response.json().get('detail') == 'Product with sku incorrect_sku not found'
    app.dependency_overrides = {}


def test_create_product_return_200_status(product_image, product_route_dependencies_mock):
    # noinspection PyUnresolvedReferences
    app.dependency_overrides[ProductController] = ProductControllerMock
    response = client.post(
        '/products',
        data={'sku': '789', 'name': 'Product 789', 'description': 'Description 789', 'price': 789.0},
        files={'image': ("product_image.png", product_image, "image/png")}
    )
    assert response.status_code == 200
    assert response.json().get('sku') == "789"
    assert response.json().get('name') == "Product 789"
    assert response.json().get('description') == "Description 789"
    assert response.json().get('price') == 789.0
    assert response.json().get('image_url') == "https://example.com/789.png"
    product_image.close()
    app.dependency_overrides = {}


def test_create_product_return_400_status_with_existing_sku(product_image, product_route_dependencies_mock):
    # noinspection PyUnresolvedReferences
    app.dependency_overrides[ProductController] = ProductControllerMock
    response = client.post(
        '/products',
        data={'sku': '123', 'name': 'Product 123', 'description': 'Description 123', 'price': 123.0},
        files={'image': ("product_image.png", product_image, "image/png")}
    )
    assert response.status_code == 400
    assert response.json().get('detail') == 'Product with sku 123 already exists'
    product_image.close()
    app.dependency_overrides = {}


def test_create_product_return_500_status_with_incorrect_image(product_image, product_route_dependencies_mock):
    # noinspection PyUnresolvedReferences
    app.dependency_overrides[ProductController] = ProductControllerMock
    response = client.post(
        '/products',
        data={'sku': '789', 'name': 'Product 789', 'description': 'Description 789', 'price': 789.0},
        files={'image': ("bad_image.png", product_image, "image/png")}
    )
    assert response.status_code == 500
    assert response.json().get('detail') == 'Could not upload file'
    product_image.close()
    app.dependency_overrides = {}


def test_update_product_return_200_status(product_image, product_route_dependencies_mock):
    # noinspection PyUnresolvedReferences
    app.dependency_overrides[ProductController] = ProductControllerMock
    response = client.put(
        '/products',
        data={'sku': '123', 'name': 'Product 123 changed', 'description': 'Description 123 changed', 'price': 321.0},
        files={'image': ("product_image.png", product_image, "image/png")}
    )
    assert response.status_code == 200
    assert response.json().get('sku') == "123"
    assert response.json().get('name') == "Product 123 changed"
    assert response.json().get('description') == "Description 123 changed"
    assert response.json().get('price') == 321.0
    assert response.json().get('image_url') == "https://example.com/123.png"
    product_image.close()
    app.dependency_overrides = {}


def test_update_product_return_404_status_with_incorrect_sku(product_image, product_route_dependencies_mock):
    # noinspection PyUnresolvedReferences
    app.dependency_overrides[ProductController] = ProductControllerMock
    response = client.put(
        '/products',
        data={'sku': 'incorrect_sku', 'name': 'Product 123 changed', 'description': 'Description 123 changed',
              'price': 321.0},
        files={'image': ("product_image.png", product_image, "image/png")}
    )
    assert response.status_code == 404
    assert response.json().get('detail') == 'Product with sku incorrect_sku not found'
    product_image.close()
    app.dependency_overrides = {}


def test_update_product_return_500_status_with_incorrect_image(product_image, product_route_dependencies_mock):
    # noinspection PyUnresolvedReferences
    app.dependency_overrides[ProductController] = ProductControllerMock
    response = client.put(
        '/products',
        data={'sku': '123', 'name': 'Product 123 changed', 'description': 'Description 123 changed', 'price': 321.0},
        files={'image': ("bad_image.png", product_image, "image/png")}
    )
    assert response.status_code == 500
    assert response.json().get('detail') == 'Could not upload file'
    product_image.close()
    app.dependency_overrides = {}


def test_delete_product_return_200_status(product_route_dependencies_mock):
    response = client.delete('/products/123')
    assert_200_response(response)
    app.dependency_overrides = {}


def test_delete_product_return_404_status_with_incorrect_sku(product_route_dependencies_mock):
    response = client.delete('/products/incorrect_sku')
    assert response.status_code == 404
    assert response.json().get('detail') == 'Product with sku incorrect_sku not found'
    app.dependency_overrides = {}
