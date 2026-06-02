import asyncio
from app.core.database import engine, Base
import app.models.user
import app.models.expense
import app.models.budget
import app.models.goal
import app.models.personality
import app.models.recommendation
import app.models.stress_score
import app.models.alert

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())
