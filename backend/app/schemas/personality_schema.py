from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class InsightsResponse(BaseModel):
    personality_summary: str
    financial_habits: str
    behavioral_risks: str
    growth_opportunities: str
    recommended_challenges: List[str]

class PersonalityInput(BaseModel):
    user_id: Optional[str] = Field("default_user", description="Unique user identifier")
    monthly_income: float = Field(..., gt=0.0, description="Monthly income")
    savings_rate: float = Field(..., ge=0.0, le=1.0, description="Monthly savings rate")
    stress_score: float = Field(..., ge=0.0, le=100.0, description="Stress Score (0-100)")
    weekend_ratio: float = Field(..., ge=0.0, description="Weekend ratio")
    impulse_score: float = Field(..., ge=0.0, le=1.0, description="Impulse spending score")
    goal_completion_rate: float = Field(..., ge=0.0, le=1.0, description="Goal completion rate")
    budget_adherence: float = Field(..., ge=0.0, le=1.0, description="Budget adherence rate")
    spending_volatility: float = Field(..., ge=0.0, description="Spending volatility index")
    subscription_count: int = Field(..., ge=0, description="Active subscription count")
    category_distribution: Dict[str, float] = Field(..., description="Category spending distributions")

class PersonalityResponse(BaseModel):
    personality_type: str
    confidence: float
    strengths: List[str]
    weaknesses: List[str]
    improvement_plan: List[str]
    coaching_style: str
    insights: InsightsResponse

class DashboardResponse(BaseModel):
    type: str
    confidence: int
    primary_color: str
    summary: str
