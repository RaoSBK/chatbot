from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class BudgetCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: str = Field(..., min_length=1, max_length=100)
    monthly_limit: Decimal = Field(..., gt=0)

class BudgetUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: Optional[str] = Field(None, min_length=1, max_length=100)
    monthly_limit: Optional[Decimal] = Field(None, gt=0)

class BudgetResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    budget_id: UUID
    user_id: UUID
    category: str
    monthly_limit: Decimal
    current_spending: Decimal
    remaining_amount: Decimal
    created_at: datetime
    updated_at: datetime
