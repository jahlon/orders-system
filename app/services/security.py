from datetime import timedelta, datetime
from typing import Annotated

from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

# noinspection PyPackageRequirements
from jose import jwt, JWTError

from passlib.context import CryptContext
from pydantic import BaseModel
from starlette import status

from app.config import Settings, get_settings
from app.data.errors import UserNotFoundError, IncorrectPasswordError
from app.data.models import User
from app.services.impl import UserService
from app.services.interfaces import IUserService


# Constant values for JWT
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    """
    Token model for JWT
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Model to validate data from JWT token
    """
    username: str | None = None
    scopes: list[str] = []


# Passlib context for hashing passwords
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# OAuth2 flow for authentication with Bearer token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes={
        "me": "Read information about the current user.",
        "product_read": "Read products",
        "product_write": "Create, update and delete products",
        "user_order_read": "Read orders of the current user",
        "order_read": "Read all orders",
        "order_write": "Create orders",
        "user_write": "Create users",
    }
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if given password matches the hashed one
    :param plain_password: Password to verify
    :param hashed_password: Hashed password
    :return: True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Get the hash of a given password
    :param password: Password to hash
    :return: Hashed password
    """
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str,
                      user_service: IUserService) -> User:
    """
    Authenticate a user by username and password
    :param username: Username of the user
    :param password: Password of the user
    :param user_service: User service dependency
    :return: User if authentication is successful
    :raises UserNotFoundError: If user is not found
    :raises IncorrectPasswordError: If password is incorrect
    """
    try:
        user = user_service.get_by_username(username)
    except UserNotFoundError:
        raise
    else:
        if not verify_password(password, user.hashed_password):
            raise IncorrectPasswordError
        return user


def create_access_token(data: dict, settings: Settings, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT token with given data
    :param data: Data to encode in the token
    :param settings: Settings dependency
    :param expires_delta: Time delta for the token to expire
    :return: JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_encoding_key, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(security_scopes: SecurityScopes,
                           token: Annotated[str, Depends(oauth2_scheme)],
                           user_service: Annotated[UserService, Depends(UserService)],
                           settings: Annotated[Settings, Depends(get_settings)]) -> User:
    """
    Get the current user from the JWT token.

    This methods gets called by FastAPI's Security dependency.
    It will check if the token is valid and if the user has the required scopes.

    :param security_scopes: Security scopes of the token
    :param token: JWT token
    :param user_service: User service dependency
    :param settings: Settings dependency
    :return: User if authentication is successful
    :raises HTTPException: If authentication fails
    """

    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = 'Bearer'

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        # Decode the token and get the username and scopes
        payload = jwt.decode(token, settings.jwt_encoding_key, algorithms=[ALGORITHM])
        username: str = payload.get('sub')  # sub is the username
        if username is None:
            raise credentials_exception
        token_scopes = payload.get('scopes', [])
        # Create a TokenData object with the username and scopes
        token_data = TokenData(scopes=token_scopes, username=username)
    except JWTError:
        raise credentials_exception
    else:
        try:
            # If the token is valid, get the user from the database
            user = user_service.get_by_username(token_data.username)
        except UserNotFoundError:
            raise credentials_exception
        else:
            # Check if the user has the required scopes
            for scope in security_scopes.scopes:
                if scope not in token_data.scopes:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Not enough permissions',
                        headers={'WWW-Authenticate': authenticate_value}
                    )
            return user


async def get_current_active_user(current_user: Annotated[User, Security(get_current_user, scopes=["me"])]) -> User:
    """
    Get the current active user. This method depends on the get_current_user method.
    After the user is authenticated, this method will check if the user is active.
    :param current_user: get_current_user dependency
    :return: User if authentication is successful
    :raises HTTPException: If user is not active
    """
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inactive user')
    return current_user
