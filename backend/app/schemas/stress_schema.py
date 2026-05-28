from typing import List, Optional
from pydantic import BaseModel, Field

class StressInput(BaseModel):
    user_id: Optional[str] = Field("default_user", description="Unique user identifier")
    monthly_income: float = Field(..., gt=0.0, description="Monthly income")
    monthly_expenses: float = Field(..., ge=0.0, description="Monthly expenses")
    savings: float = Field(..., ge=0.0, description="Savings amount")
    goal_progress: float = Field(..., ge=0.0, le=100.0, description="Goal completion percentage")
    weekend_ratio: float = Field(..., ge=0.0, description="Weekend spending ratio")
    impulse_score: float = Field(..., ge=0.0, le=1.0, description="Impulse spending score")
    spending_volatility: float = Field(..., ge=0.0, description="Spending volatility index")
    subscription_count: int = Field(..., ge=0, description="Active subscriptions count")
    budget_utilization: float = Field(..., ge=0.0, description="Budget utilization percentage")
    category_spikes: int = Field(..., ge=0, description="Count of category surges")

class StressResponse(BaseModel):
    stress_score: int
    stress_level: str
    confidence: float
    risk_factors: List[str]
    recommendations: List[str]

class SummaryResponse(BaseModel):
    gauge_score: int
    trend: str
    stress_level: str
