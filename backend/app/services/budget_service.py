from uuid import UUID
from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.budget_repo import BudgetRepository
from app.schemas.budget import BudgetCreate, BudgetUpdate
from app.models.budget import Budget

class BudgetService:
    def __init__(self, repo: BudgetRepository):
        self.repo = repo

    async def create_budget(self, budget_in: BudgetCreate, user_id: UUID) -> Budget:
        return await self.repo.create(budget_in.model_dump(), user_id)

    async def get_budget(self, budget_id: UUID, user_id: UUID) -> Budget:
        budget = await self.repo.get_by_id(budget_id, user_id)
        if not budget:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Budget not found"
            )
        return budget

    async def get_all_budgets(self, user_id: UUID, skip: int = 0, limit: int = 20) -> List[Budget]:
        return await self.repo.get_all(user_id, skip=skip, limit=limit)

    async def update_budget(self, budget_id: UUID, budget_in: BudgetUpdate, user_id: UUID) -> Budget:
        budget = await self.repo.get_by_id(budget_id, user_id)
        if not budget:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Budget not found"
            )
        update_data = budget_in.model_dump(exclude_unset=True)
        return await self.repo.update(budget, update_data)

    async def delete_budget(self, budget_id: UUID, user_id: UUID) -> Budget:
        budget = await self.repo.get_by_id(budget_id, user_id)
        if not budget:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Budget not found"
            )
        return await self.repo.delete(budget)
