from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

from stress_calculator import evaluate_stress

app = FastAPI(
    title="MoneyMind X Financial Stress Score Engine",
    description="ML and rule-based API predicting and classifying financial stress scores.",
    version="1.0.0"
)

# In-memory database of analysis history (user_id -> List of past reports)
STRESS_HISTORY: Dict[str, List[Dict[str, Any]]] = {}

# ----------------------------------------------------
# Pydantic Schemas
# ----------------------------------------------------
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

# ----------------------------------------------------
# API Endpoints
# ----------------------------------------------------
@app.post("/stress/analyze", response_model=StressResponse, status_code=status.HTTP_200_OK)
async def analyze_stress(payload: StressInput):
    """
    Analyzes user financial indicators, detects risk factors, and computes the stress score.
    """
    user_id = payload.user_id or "default_user"
    raw_data = payload.model_dump()
    
    try:
        report = evaluate_stress(raw_data)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Stress score calculation failed: {e}"
        )

    # Persist in-memory history (max last 5 records per user)
    if user_id not in STRESS_HISTORY:
        STRESS_HISTORY[user_id] = []
        
    STRESS_HISTORY[user_id].append(report)
    if len(STRESS_HISTORY[user_id]) > 5:
        STRESS_HISTORY[user_id].pop(0)

    return StressResponse(**report)

@app.get("/stress/history", status_code=status.HTTP_200_OK)
async def get_stress_history(user_id: str = Query(..., min_length=1, description="Unique user identifier")):
    """
    Retrieves the chronological history of past stress evaluations for the specified user.
    """
    history = STRESS_HISTORY.get(user_id, [])
    return {
        "user_id": user_id,
        "history_count": len(history),
        "history": history
    }

@app.get("/stress/summary", response_model=SummaryResponse, status_code=status.HTTP_200_OK)
async def get_stress_summary(user_id: str = Query(..., min_length=1, description="Unique user identifier")):
    """
    Generates a dashboard-ready visualization summary containing the latest gauge score, trend, and level.
    """
    history = STRESS_HISTORY.get(user_id, [])
    if not history:
        raise HTTPException(
            status_code=404,
            detail=f"No stress evaluation history found for user '{user_id}'."
        )
        
    latest = history[-1]
    
    # Calculate Trend based on past history (Comparing latest with previous if available)
    if len(history) >= 2:
        prev = history[-2]
        latest_score = latest["stress_score"]
        prev_score = prev["stress_score"]
        
        # A higher score represents a healthier state (improving)
        if latest_score > prev_score:
            trend = "Improving"
        elif latest_score < prev_score:
            trend = "Declining"
        else:
            trend = "Stable"
    else:
        trend = "Stable" # Default for first analysis

    return SummaryResponse(
        gauge_score=latest["stress_score"],
        trend=trend,
        stress_level=latest["stress_level"]
    )
