from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.budget import Budget

class BudgetRepository(BaseRepository[Budget]):
    def __init__(self, db: AsyncSession):
        super().__init__(Budget, db)
