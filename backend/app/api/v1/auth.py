from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.limiter import limiter
from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService
from app.schemas.auth import UserRegister, UserResponse, TokenResponse, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def register(
    request: Request,
    user_in: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    return await auth_service.register(user_in)

@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    credentials = UserLogin(email=form_data.username, password=form_data.password)
    return await auth_service.authenticate(credentials)
