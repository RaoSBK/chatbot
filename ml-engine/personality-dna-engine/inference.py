from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

from feature_engineering import engineer_features
from ensemble_model import get_personality_profile
from config import ARCHETYPES_METADATA

app = FastAPI(
    title="MoneyMind X Financial Personality DNA Engine",
    description="ML and rule-based API classifying and personalizing user financial personality archetypes.",
    version="1.0.0"
)

# In-memory database of analysis history (user_id -> List of past reports)
PERSONALITY_HISTORY: Dict[str, List[Dict[str, Any]]] = {}

# ----------------------------------------------------
# Pydantic Schemas
# ----------------------------------------------------
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

class InsightsResponse(BaseModel):
    personality_summary: str
    financial_habits: str
    behavioral_risks: str
    growth_opportunities: str
    recommended_challenges: List[str]

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

# ----------------------------------------------------
# API Endpoints
# ----------------------------------------------------
@app.post("/personality/analyze", response_model=PersonalityResponse, status_code=status.HTTP_200_OK)
async def analyze_personality(payload: PersonalityInput):
    """
    Analyzes user financial behavioral metrics, maps personality features,
    and runs the ensemble decision layer to predict user financial DNA.
    """
    user_id = payload.user_id or "default_user"
    raw_data = payload.model_dump()

    try:
        # 1. Feature Engineering
        features = engineer_features(raw_data)
        
        # 2. Ensemble Classification
        profile = get_personality_profile(raw_data, features)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Financial Personality classification failed: {e}"
        )

    # Persist in-memory history (max last 5 records per user)
    if user_id not in PERSONALITY_HISTORY:
        PERSONALITY_HISTORY[user_id] = []
        
    PERSONALITY_HISTORY[user_id].append(profile)
    if len(PERSONALITY_HISTORY[user_id]) > 5:
        PERSONALITY_HISTORY[user_id].pop(0)

    return PersonalityResponse(**profile)

@app.get("/personality/profile", response_model=DashboardResponse, status_code=status.HTTP_200_OK)
async def get_personality_profile_dashboard(user_id: str = Query(..., min_length=1, description="Unique user identifier")):
    """
    Generates a dashboard-ready financial profile, gauge confidence, primary brand color, and core summary.
    """
    history = PERSONALITY_HISTORY.get(user_id, [])
    if not history:
        raise HTTPException(
            status_code=404,
            detail=f"No financial personality history found for user '{user_id}'."
        )
        
    latest = history[-1]
    ptype = latest["personality_type"]
    
    meta = ARCHETYPES_METADATA.get(ptype, ARCHETYPES_METADATA["Planner"])
    
    return DashboardResponse(
        type=ptype,
        confidence=int(round(latest["confidence"] * 100)),
        primary_color=meta["primary_color"],
        summary=meta["summary"]
    )

@app.get("/personality/history", status_code=status.HTTP_200_OK)
async def get_personality_history(user_id: str = Query(..., min_length=1, description="Unique user identifier")):
    """
    Retrieves the chronological history of past personality classifications for the specified user.
    """
    history = PERSONALITY_HISTORY.get(user_id, [])
    return {
        "user_id": user_id,
        "history_count": len(history),
        "history": history
    }
