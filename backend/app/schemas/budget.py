from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class BudgetCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: str = Field(..., min_length=1, max_length=100)
    amount: Decimal = Field(..., gt=0)
    start_date: date
    end_date: date

class BudgetUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: Optional[str] = Field(None, min_length=1, max_length=100)
    amount: Optional[Decimal] = Field(None, gt=0)
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class BudgetResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: UUID
    user_id: UUID
    category: str
    amount: Decimal
    start_date: date
    end_date: date
    created_at: datetime
