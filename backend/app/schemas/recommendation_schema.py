import datetime
from decimal import Decimal
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict

class ExpenseInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    amount: Decimal = Field(..., gt=0, description="Amount of the expense")
    category: str = Field(..., min_length=1, max_length=100, description="Category of the expense")
    date: datetime.date = Field(..., description="Date of the expense (YYYY-MM-DD)")
    description: Optional[str] = Field(None, max_length=255, description="Short description of the expense")

class RecommendationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    monthly_income: Decimal = Field(..., gt=0, description="User's monthly income")
    expenses: List[ExpenseInput] = Field(..., description="List of expenses to analyze")

class RecommendationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    recommendation_type: str = Field(..., description="The category or type of spending being addressed")
    severity: Literal["Low", "Medium", "High"] = Field(..., description="Severity level of the spending issue")
    possible_savings: Decimal = Field(..., description="Calculated potential monthly savings")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the recommendation")
    recommendation: str = Field(..., description="Actionable recommendation description")
    reason: str = Field(..., description="Detailed explanation/reasoning for the recommendation")
