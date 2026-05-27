from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class GoalCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    goal_name: str = Field(..., min_length=1, max_length=255)
    target_amount: Decimal = Field(..., gt=0)
    saved_amount: Optional[Decimal] = Field(Decimal("0.00"), ge=0)
    target_date: date

class GoalUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    goal_name: Optional[str] = Field(None, min_length=1, max_length=255)
    target_amount: Optional[Decimal] = Field(None, gt=0)
    saved_amount: Optional[Decimal] = Field(None, ge=0)
    target_date: Optional[date] = None
    status: Optional[str] = None

class GoalResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    goal_id: UUID
    user_id: UUID
    goal_name: str
    target_amount: Decimal
    saved_amount: Decimal
    target_date: date
    progress_percentage: float
    status: str
    created_at: datetime
    updated_at: datetime
