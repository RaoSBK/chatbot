from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, Request, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.limiter import limiter
from app.models.user import User
from app.repositories.expense_repo import ExpenseRepository
from app.services.expense_service import ExpenseService
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("100/minute")
async def create_expense(
    request: Request,
    expense_in: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = ExpenseRepository(db)
    service = ExpenseService(repo)
    return await service.create_expense(expense_in, current_user.id)

@router.get("", response_model=List[ExpenseResponse])
@limiter.limit("100/minute")
async def get_expenses(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = ExpenseRepository(db)
    service = ExpenseService(repo)
    return await service.get_all_expenses(current_user.id, skip=skip, limit=limit)

@router.get("/{expense_id}", response_model=ExpenseResponse)
@limiter.limit("100/minute")
async def get_expense(
    request: Request,
    expense_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = ExpenseRepository(db)
    service = ExpenseService(repo)
    return await service.get_expense(expense_id, current_user.id)

@router.put("/{expense_id}", response_model=ExpenseResponse)
@limiter.limit("100/minute")
async def update_expense(
    request: Request,
    expense_id: UUID,
    expense_in: ExpenseUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = ExpenseRepository(db)
    service = ExpenseService(repo)
    return await service.update_expense(expense_id, expense_in, current_user.id)

@router.delete("/{expense_id}", response_model=ExpenseResponse)
@limiter.limit("100/minute")
async def delete_expense(
    request: Request,
    expense_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = ExpenseRepository(db)
    service = ExpenseService(repo)
    return await service.delete_expense(expense_id, current_user.id)
