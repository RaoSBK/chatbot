import asyncio
from app.core.database import Base, engine
from app.models.user import User
from app.models.expense import Expense
from app.models.budget import Budget
from app.models.goal import Goal
from app.models.personality import Personality
from app.models.recommendation import Recommendation
from app.models.stress_score import Stress_score
from app.models.alert import Alert

async def init_db():
    print("Initializing database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())
