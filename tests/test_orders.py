import pytest
from fastapi.testclient import TestClient

from app.data.models import User
from app.main import app
from tests.mocks.services_mocks import OrderServiceMock
from app.services.security import get_current_user
from app.services.impl import OrderService

ORDERS = '/orders'

client = TestClient(app)


def get_current_user_mock():
    return User(username='admin', email="admin@gmail.com", full_name="Administrator", disabled=False)


@pytest.fixture
def order_route_dependencies_mock():
    # noinspection PyUnresolvedReferences
    app.dependency_overrides[OrderService] = OrderServiceMock
    # noinspection PyUnresolvedReferences
    app.dependency_overrides[get_current_user] = get_current_user_mock


@pytest.fixture
def order_123():
    return {
        "id": "123",
        "products": [
            {
                "sku": "123",
                "price": 123.0,
                "quantity": 1
            },
            {
                "sku": "456",
                "price": 456.0,
                "quantity": 2
            }
        ],
        "status": "pending",
        "total": 1035.0,
        "user": "admin",
        "created_at": "2021-10-10T00:00:00Z"
    }


@pytest.fixture
def order_in():
    return {
        "products": [
            {
                "sku": "123",
                "price": 123.0,
                "quantity": 1
            },
            {
                "sku": "456",
                "price": 456.0,
                "quantity": 2
            }
        ],
        "status": "pending"
    }


@pytest.fixture
def order_out():
    return {
        "id": "123",
        "products": [
            {
                "sku": "123",
                "price": 123.0,
                "quantity": 1
            },
            {
                "sku": "456",
                "price": 456.0,
                "quantity": 2
            }
        ],
        "status": "pending",
        "total": 1035.0,
        "created_at": "2021-10-10T00:00:00Z"
    }


def test_get_all_orders_return_200_status(order_route_dependencies_mock):
    response = client.get(ORDERS)
    assert response.status_code == 200
    assert len(response.json()) == 2
    app.dependency_overrides = {}


def test_get_order_return_200_status(order_route_dependencies_mock, order_123):
    response = client.get(f'{ORDERS}/123')
    assert response.status_code == 200
    assert response.json() == order_123
    app.dependency_overrides = {}


def test_get_order_return_404_status_with_incorrect_id(order_route_dependencies_mock):
    response = client.get(f'{ORDERS}/incorrect_id')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Order with id incorrect_id not found'}
    app.dependency_overrides = {}


def test_create_order_return_200_status(order_route_dependencies_mock, order_in):
    response = client.post(
        ORDERS,
        json=order_in
    )
    assert response.status_code == 200
    assert response.json().get('products') == [
        {
            "sku": "123",
            "price": 123.0,
            "quantity": 1
        },
        {
            "sku": "456",
            "price": 456.0,
            "quantity": 2
        }
    ]
    assert response.json().get('status') == "pending"
    assert response.json().get('total') == 1035
    app.dependency_overrides = {}
