from typing import Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.limiter import limiter
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.auth import (
    AccessTokenResponse, TokenResponse, UserLogin,
    UserRegister, UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ── cookie constants ──────────────────────────────────────────────────────────
_COOKIE_NAME = "mmx_refresh_token"
_COOKIE_PATH = "/api/v1/auth"        # restrict cookie to auth routes
_COOKIE_MAX_AGE = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key=_COOKIE_NAME,
        value=refresh_token,
        httponly=True,          # JS cannot read it → XSS-safe
        secure=False,           # flip to True in production (HTTPS)
        samesite="lax",
        max_age=_COOKIE_MAX_AGE,
        path=_COOKIE_PATH,
    )


def _clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(key=_COOKIE_NAME, path=_COOKIE_PATH)


# ── endpoints ─────────────────────────────────────────────────────────────────

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user account",
)
@limiter.limit("10/minute")
async def register(
    request: Request,
    user_in: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user. Returns the created user profile (no tokens yet)."""
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    return await auth_service.register(user_in)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate and obtain JWT tokens",
)
@limiter.limit("10/minute")
async def login(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    Login with email + password.
    - Returns the **access token** in the JSON body.
    - Sets the **refresh token** as an `HttpOnly` cookie (path-restricted).
    """
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    credentials = UserLogin(email=form_data.username, password=form_data.password)
    token_data = await auth_service.authenticate(credentials)

    # Persist refresh token in a secure, HttpOnly cookie
    _set_refresh_cookie(response, token_data.refresh_token)

    return token_data  # body still includes refresh_token for non-browser clients


@router.post(
    "/refresh",
    response_model=AccessTokenResponse,
    summary="Rotate tokens using the refresh-token cookie",
)
async def refresh(
    response: Response,
    mmx_refresh_token: Optional[str] = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
):
    """
    Uses the `mmx_refresh_token` HttpOnly cookie to issue a new access token.
    The refresh token is **rotated** (old one invalidated, new one set).
    """
    if not mmx_refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token cookie not found. Please log in again.",
        )

    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    access_response, new_refresh = await auth_service.refresh(mmx_refresh_token)

    # Rotate the cookie
    _set_refresh_cookie(response, new_refresh)

    return access_response


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Invalidate session and clear the refresh-token cookie",
)
async def logout(response: Response):
    """Clear the HttpOnly refresh-token cookie to log the user out."""
    _clear_refresh_cookie(response)
    return {"message": "Logged out successfully"}


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get the authenticated user's profile",
)
async def get_me(current_user: User = Depends(get_current_user)):
    """Returns the profile of the currently authenticated user."""
    return current_user
