from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, Request, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.limiter import limiter
from app.models.user import User
from app.repositories.goal_repo import GoalRepository
from app.services.goal_service import GoalService
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse

router = APIRouter(prefix="/goals", tags=["goals"])

@router.post("", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("100/minute")
async def create_goal(
    request: Request,
    goal_in: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = GoalRepository(db)
    service = GoalService(repo)
    return await service.create_goal(goal_in, current_user.id)

@router.get("", response_model=List[GoalResponse])
@limiter.limit("100/minute")
async def get_goals(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = GoalRepository(db)
    service = GoalService(repo)
    return await service.get_all_goals(current_user.id, skip=skip, limit=limit)

@router.get("/{goal_id}", response_model=GoalResponse)
@limiter.limit("100/minute")
async def get_goal(
    request: Request,
    goal_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = GoalRepository(db)
    service = GoalService(repo)
    return await service.get_goal(goal_id, current_user.id)

@router.put("/{goal_id}", response_model=GoalResponse)
@limiter.limit("100/minute")
async def update_goal(
    request: Request,
    goal_id: UUID,
    goal_in: GoalUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = GoalRepository(db)
    service = GoalService(repo)
    return await service.update_goal(goal_id, goal_in, current_user.id)

@router.delete("/{goal_id}", response_model=GoalResponse)
@limiter.limit("100/minute")
async def delete_goal(
    request: Request,
    goal_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = GoalRepository(db)
    service = GoalService(repo)
    return await service.delete_goal(goal_id, current_user.id)
