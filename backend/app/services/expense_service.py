from uuid import UUID
from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.expense_repo import ExpenseRepository
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from app.models.expense import Expense

class ExpenseService:
    def __init__(self, repo: ExpenseRepository):
        self.repo = repo

    async def create_expense(self, expense_in: ExpenseCreate, user_id: UUID) -> Expense:
        return await self.repo.create(expense_in.model_dump(), user_id)

    async def get_expense(self, expense_id: UUID, user_id: UUID) -> Expense:
        expense = await self.repo.get_by_id(expense_id, user_id)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        return expense

    async def get_all_expenses(self, user_id: UUID, skip: int = 0, limit: int = 20) -> List[Expense]:
        return await self.repo.get_all(user_id, skip=skip, limit=limit)

    async def update_expense(self, expense_id: UUID, expense_in: ExpenseUpdate, user_id: UUID) -> Expense:
        expense = await self.repo.get_by_id(expense_id, user_id)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        # Filter out unset/None fields during update if needed, but since we support partial update,
        # we update only what is provided in the input model_dump(exclude_unset=True)
        update_data = expense_in.model_dump(exclude_unset=True)
        return await self.repo.update(expense, update_data)

    async def delete_expense(self, expense_id: UUID, user_id: UUID) -> Expense:
        expense = await self.repo.get_by_id(expense_id, user_id)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        return await self.repo.delete(expense)
