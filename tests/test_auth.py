import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.impl import UserService
from tests.mocks.services_mocks import UserServiceMock

client = TestClient(app)


@pytest.fixture
def user_service_mock():
    # noinspection PyUnresolvedReferences
    app.dependency_overrides[UserService] = UserServiceMock


def test_login_for_access_token_return_access_token_with_200_status(user_service_mock):
    response = client.post(
        '/auth/token',
        data={'username': 'admin', 'password': 'admin'}
    )
    assert response.status_code == 200
    assert response.json().get('access_token')
    assert response.json().get('token_type') == 'bearer'
    app.dependency_overrides = {}


def test_login_for_access_token_return_401_status_with_incorrect_password(user_service_mock):
    response = client.post(
        '/auth/token',
        data={'username': 'admin', 'password': 'wrong_password'}
    )
    assert response.status_code == 401
    assert response.json().get('detail') == 'Incorrect username or password'
    app.dependency_overrides = {}


def test_login_for_access_token_return_401_status_with_incorrect_username(user_service_mock):
    response = client.post(
        '/auth/token',
        data={'username': 'wrong_username', 'password': 'admin'}
    )
    assert response.status_code == 401
    assert response.json().get('detail') == 'Incorrect username or password'
    app.dependency_overrides = {}


def test_read_users_me_return_user_with_200_status(user_service_mock):
    response = client.post(
        '/auth/token',
        data={'username': 'admin', 'password': 'admin'}
    )
    access_token = response.json().get('access_token')
    response = client.get(
        '/auth/users/me',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 200
    assert response.json().get('username') == "admin"
    assert response.json().get('email') == "admin@gmail.com"
    assert response.json().get('full_name') == "Administrator"
    assert response.json().get('disabled') is False
    app.dependency_overrides = {}


def test_read_users_me_return_401_status_with_incorrect_token(user_service_mock):
    response = client.get(
        '/auth/users/me',
        headers={'Authorization': f'Bearer incorrect_token'}
    )
    assert response.status_code == 401
    assert response.json().get('detail') == 'Could not validate credentials'
    app.dependency_overrides = {}


def test_read_users_me_return_401_status_with_incorrect_scopes(user_service_mock):
    response = client.post(
        '/auth/token',
        data={'username': 'user', 'password': 'user'}
    )
    access_token = response.json().get('access_token')
    response = client.get(
        '/auth/users/me',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 401
    assert response.json().get('detail') == 'Not enough permissions'
    app.dependency_overrides = {}
