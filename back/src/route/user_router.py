"""
users endpoint
"""
from fastapi import status
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..apps.auth.model.domain.user import User
from ..apps.auth.model.schema.user import UserCreateRequest, UserCreatedResponse, UserSignInResponse
from ..apps.auth.service.user import create_user
from ..apps.auth.service.auth import authenticate_user
from ..apps.auth.service.token import create_access_token

from ..core.database import get_database_session

from ..apps.auth.service.user import get_current_active_user

user_router = APIRouter()


@user_router.post(
    path="/signup",
    name="Sign Up",
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreatedResponse,
)
async def add_user(
        user_create_request: UserCreateRequest,
        db: Session = Depends(get_database_session),
) -> UserCreatedResponse:
    """ Add User """
    try:
        new_user: User = await create_user(
            username=user_create_request.username,
            email=user_create_request.email,
            full_name=user_create_request.full_name,
            plain_password=user_create_request.plain_password,
            db=db,
        )
        user_created_response: UserCreatedResponse = UserCreatedResponse(
            username=new_user.username,
            email=new_user.email,
            full_name=new_user.full_name,
            created_at=new_user.created_at,
        )
        return user_created_response
    except ValueError as err:
        raise HTTPException(
            status_code=400,
            detail=str(err),
        )
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail=str(err),
        )


@user_router.post(
    path="/signin",
    name="Sign In",
    status_code=status.HTTP_200_OK,
    response_model=UserSignInResponse,
)
async def sign_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_database_session),
) -> UserSignInResponse:
    try:
        user = await authenticate_user(
            db=db,
            email=form_data.username,
            password=form_data.password,
        )

        token, token_type = await create_access_token(
            user_id=user.id,
            scopes=user.scopes,
        )

        if not token:
            raise ValueError("Invalid token")

        signin_response = UserSignInResponse(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            access_token=token,
            token_type=token_type,
        )

        return signin_response
    except ValueError as err:
        raise HTTPException(
            status_code=400,
            detail=str(err),
        )
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail=str(err),
        )
