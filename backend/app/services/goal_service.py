from uuid import UUID
from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.goal_repo import GoalRepository
from app.schemas.goal import GoalCreate, GoalUpdate
from app.models.goal import Goal

class GoalService:
    def __init__(self, repo: GoalRepository):
        self.repo = repo

    async def create_goal(self, goal_in: GoalCreate, user_id: UUID) -> Goal:
        return await self.repo.create(goal_in.model_dump(), user_id)

    async def get_goal(self, goal_id: UUID, user_id: UUID) -> Goal:
        goal = await self.repo.get_by_id(goal_id, user_id)
        if not goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Goal not found"
            )
        return goal

    async def get_all_goals(self, user_id: UUID, skip: int = 0, limit: int = 20) -> List[Goal]:
        return await self.repo.get_all(user_id, skip=skip, limit=limit)

    async def update_goal(self, goal_id: UUID, goal_in: GoalUpdate, user_id: UUID) -> Goal:
        goal = await self.repo.get_by_id(goal_id, user_id)
        if not goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Goal not found"
            )
        update_data = goal_in.model_dump(exclude_unset=True)
        return await self.repo.update(goal, update_data)

    async def delete_goal(self, goal_id: UUID, user_id: UUID) -> Goal:
        goal = await self.repo.get_by_id(goal_id, user_id)
        if not goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Goal not found"
            )
        return await self.repo.delete(goal)
