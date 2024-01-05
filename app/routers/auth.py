from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.backend.session import create_session
from app.const import (
    AUTH_TAGS,
    AUTH_URL, AUTH_REG_URL,
)
from app.schemas.auth import TokenSchema, CreateUserSchema, UserSchema
from app.services.auth import AuthService


router = APIRouter(prefix="", tags=AUTH_TAGS)


@router.post("/" + AUTH_URL, response_model=TokenSchema)
async def authenticate(
    login: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(create_session),
) -> TokenSchema | None:
    """User authentication.

    Raises:
        HTTPException: 401 Unauthorized
        HTTPException: 404 Not Found

    Returns:
        Access token.
    """

    return AuthService(session).authenticate(login)


@router.post("/" + AUTH_REG_URL, status_code=status.HTTP_201_CREATED)
async def registration(
    item: CreateUserSchema,
    session: Session = Depends(create_session),
) -> UserSchema:
    """User registration.

    Raises:
        HTTPException: 400 Bad request
            - The user with specified email address already exists
    """

    model = AuthService(session).create_user(item)
    return AuthService(session).get_user(model.email)
