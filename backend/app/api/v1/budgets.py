from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, Request, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.limiter import limiter
from app.models.user import User
from app.repositories.budget_repo import BudgetRepository
from app.services.budget_service import BudgetService
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetResponse

router = APIRouter(prefix="/budgets", tags=["budgets"])

@router.post("", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("100/minute")
async def create_budget(
    request: Request,
    budget_in: BudgetCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = BudgetRepository(db)
    service = BudgetService(repo)
    return await service.create_budget(budget_in, current_user.id)

@router.get("", response_model=List[BudgetResponse])
@limiter.limit("100/minute")
async def get_budgets(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = BudgetRepository(db)
    service = BudgetService(repo)
    return await service.get_all_budgets(current_user.id, skip=skip, limit=limit)

@router.get("/{budget_id}", response_model=BudgetResponse)
@limiter.limit("100/minute")
async def get_budget(
    request: Request,
    budget_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = BudgetRepository(db)
    service = BudgetService(repo)
    return await service.get_budget(budget_id, current_user.id)

@router.put("/{budget_id}", response_model=BudgetResponse)
@limiter.limit("100/minute")
async def update_budget(
    request: Request,
    budget_id: UUID,
    budget_in: BudgetUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = BudgetRepository(db)
    service = BudgetService(repo)
    return await service.update_budget(budget_id, budget_in, current_user.id)

@router.delete("/{budget_id}", response_model=BudgetResponse)
@limiter.limit("100/minute")
async def delete_budget(
    request: Request,
    budget_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = BudgetRepository(db)
    service = BudgetService(repo)
    return await service.delete_budget(budget_id, current_user.id)
