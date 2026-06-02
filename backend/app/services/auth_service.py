from uuid import UUID
from fastapi import HTTPException, status
from jose import JWTError

from app.repositories.user_repo import UserRepository
from app.schemas.auth import (
    UserRegister, UserLogin, TokenResponse,
    AccessTokenResponse, UserResponse
)
from app.core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token
)


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, user_in: UserRegister) -> UserResponse:
        """Create a new user account. Raises 400 if email already in use."""
        existing = await self.user_repo.get_by_email(user_in.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        hashed_pwd = hash_password(user_in.password)
        user = await self.user_repo.create(
            full_name=user_in.full_name,
            email=user_in.email,
            password_hash=hashed_pwd
        )
        return user

    async def authenticate(self, credentials: UserLogin) -> TokenResponse:
        """Verify credentials and return both tokens."""
        user = await self.user_repo.get_by_email(credentials.email)
        if not user or not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(user_id=user.id)
        refresh_token = create_refresh_token(user_id=user.id)
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    async def refresh(self, refresh_token: str) -> AccessTokenResponse:
        """
        Validate the refresh token from the HttpOnly cookie and issue a
        fresh access token (+ rotate the refresh token for forward secrecy).
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
        try:
            payload = decode_token(refresh_token)
            user_id_str: str = payload.get("sub")
            token_type: str = payload.get("type", "")
            if not user_id_str or token_type != "refresh":
                raise credentials_exception
            user_id = UUID(user_id_str)
        except (JWTError, ValueError):
            raise credentials_exception

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise credentials_exception

        new_access = create_access_token(user_id=user.id)
        new_refresh = create_refresh_token(user_id=user.id)
        # new_refresh is returned so the router can rotate the cookie
        return AccessTokenResponse(
            access_token=new_access,
            token_type="bearer"
        ), new_refresh
