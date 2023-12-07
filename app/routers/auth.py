from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.config import Settings, get_settings
from app.controllers.user_controller import UserController
from app.data.errors import UserNotFoundError, IncorrectPasswordError
from app.data.models import User, UserIn
from app.services.impl import UserService
from app.services.interfaces import IUserService
from app.services.security import Token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    get_current_active_user

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={404: {'description': 'Not found'}},
)


@router.post("/users", response_model=User, dependencies=[Security(get_current_active_user, scopes=["user_write"])])
async def register_user(user: UserIn, controller: Annotated[UserController, Depends()]):
    try:
        controller.get_by_username(user.username)
    except UserNotFoundError:
        user = controller.register_user(user)
        data = dict(user)
        data.pop('hashed_password')
        data.pop('scopes')
        return User(**data)
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User already exists',
        )


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 user_service: Annotated[IUserService, Depends(UserService)],
                                 settings: Annotated[Settings, Depends(get_settings)]):
    try:
        user = authenticate_user(form_data.username, form_data.password, user_service)
    except (UserNotFoundError, IncorrectPasswordError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    else:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={'sub': user.username, "scopes": user.scopes.split()},
            settings=settings,
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user
