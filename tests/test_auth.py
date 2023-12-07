import pytest
from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.main import app
from app.services.impl import UserService
from tests.mocks.services_mocks import UserServiceMock

AUTH_USERS_ME = '/auth/users/me'
AUTH_TOKEN = '/auth/token'
AUTH_USERS = '/auth/users'

client = TestClient(app)


@pytest.fixture
def user_service_mock():
    # noinspection PyUnresolvedReferences
    app.dependency_overrides[UserService] = UserServiceMock


def get_testing_settings():
    return Settings(_env_file='.env.test', _env_file_encoding='utf-8', _extra='allow')


@pytest.fixture
def testing_settings():
    # noinspection PyUnresolvedReferences
    app.dependency_overrides[get_settings] = get_testing_settings


def test_login_for_access_token_return_access_token_with_200_status(user_service_mock):
    response = client.post(
        AUTH_TOKEN,
        data={'username': 'admin', 'password': 'admin'}
    )
    assert response.status_code == 200
    assert response.json().get('access_token')
    assert response.json().get('token_type') == 'bearer'
    app.dependency_overrides = {}


def test_login_for_access_token_return_401_status_with_incorrect_password(user_service_mock):
    response = client.post(
        AUTH_TOKEN,
        data={'username': 'admin', 'password': 'wrong_password'}
    )
    assert response.status_code == 401
    assert response.json().get('detail') == 'Incorrect username or password'
    app.dependency_overrides = {}


def test_login_for_access_token_return_401_status_with_incorrect_username(user_service_mock):
    response = client.post(
        AUTH_TOKEN,
        data={'username': 'wrong_username', 'password': 'admin'}
    )
    assert response.status_code == 401
    assert response.json().get('detail') == 'Incorrect username or password'
    app.dependency_overrides = {}


def test_read_users_me_return_user_with_200_status(user_service_mock):
    response = client.post(
        AUTH_TOKEN,
        data={'username': 'admin', 'password': 'admin'}
    )
    access_token = response.json().get('access_token')
    response = client.get(
        AUTH_USERS_ME,
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
        AUTH_USERS_ME,
        headers={'Authorization': 'Bearer incorrect_token'}
    )
    assert response.status_code == 401
    assert response.json().get('detail') == 'Could not validate credentials'
    app.dependency_overrides = {}


def test_read_users_me_return_401_status_with_incorrect_scopes(user_service_mock):
    response = client.post(
        AUTH_TOKEN,
        data={'username': 'user', 'password': 'user'}
    )
    access_token = response.json().get('access_token')
    response = client.get(
        AUTH_USERS_ME,
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 401
    assert response.json().get('detail') == 'Not enough permissions'
    app.dependency_overrides = {}


def test_register_user_return_user_with_200_status(user_service_mock):
    response = client.post(
        AUTH_TOKEN,
        data={'username': 'admin', 'password': 'admin'}
    )
    access_token = response.json().get('access_token')
    response = client.post(
        AUTH_USERS,
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'username': 'client_1',
            'password': 'client_1',
            'email': 'client_1@gmail.com',
            'full_name': 'Client 1',
            'disabled': False,
        }
    )
    assert response.status_code == 200
    assert response.json().get('username') == "client_1"
    assert response.json().get('email') == "client_1@gmail.com"
    assert response.json().get('full_name') == "Client 1"
    assert response.json().get('disabled') is False
    app.dependency_overrides = {}


def test_register_user_return_401_status_with_incorrect_token(user_service_mock):
    response = client.post(
        AUTH_USERS,
        headers={'Authorization': 'Bearer incorrect_token'},
        json={
            'username': 'client_1',
            'password': 'client_1',
            'email': 'client_1@gmail.com',
            'full_name': 'Client 1',
            'disabled': False,
        }
    )
    assert response.status_code == 401
    assert response.json().get('detail') == 'Could not validate credentials'
    app.dependency_overrides = {}


def test_register_user_return_401_status_with_incorrect_scopes(user_service_mock):
    response = client.post(
        AUTH_TOKEN,
        data={'username': 'user', 'password': 'user'}
    )
    access_token = response.json().get('access_token')
    response = client.post(
        AUTH_USERS,
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'username': 'client_1',
            'password': 'client_1',
            'email': 'client_1@gmail.com',
            'full_name': 'Client 1',
            'disabled': False,
        }
    )
    assert response.status_code == 401
    assert response.json().get('detail') == 'Not enough permissions'
    app.dependency_overrides = {}


def test_register_user_return_409_status_with_existing_username(user_service_mock):
    response = client.post(
        AUTH_TOKEN,
        data={'username': 'admin', 'password': 'admin'}
    )
    access_token = response.json().get('access_token')
    response = client.post(
        AUTH_USERS,
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'username': 'user',
            'password': 'user',
            'email': 'user@gmail.com',
            'full_name': 'User',
            'disabled': False,
        }
    )
    assert response.status_code == 409
    assert response.json().get('detail') == 'User already exists'
    app.dependency_overrides = {}
