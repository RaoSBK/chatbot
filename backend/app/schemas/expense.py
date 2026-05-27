from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class ExpenseCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    amount: Decimal = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=100)
    payment_method: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    transaction_date: date

class ExpenseUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    amount: Optional[Decimal] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    payment_method: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    transaction_date: Optional[date] = None

class ExpenseResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    expense_id: UUID
    user_id: UUID
    amount: Decimal
    category: str
    payment_method: Optional[str] = None
    description: Optional[str] = None
    transaction_date: date
    created_at: datetime
    updated_at: datetime
