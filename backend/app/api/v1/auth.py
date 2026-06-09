from fastapi import APIRouter, Depends, Request, status
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
    db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)

    credentials: UserLogin
    if request.headers.get("content-type", "").lower().startswith("application/json"):
        payload = await request.json()
        if "email" in payload:
            credentials = UserLogin(email=payload["email"], password=payload["password"])
        else:
            credentials = UserLogin(email=payload.get("username"), password=payload.get("password"))
    else:
        form_data = await request.form()
        credentials = UserLogin(email=form_data.get("username"), password=form_data.get("password"))

    return await auth_service.authenticate(credentials)
