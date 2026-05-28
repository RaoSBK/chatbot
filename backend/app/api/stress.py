from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Dict, Any
from app.schemas.stress_schema import StressInput, StressResponse, SummaryResponse
from app.services.stress_service import StressService

router = APIRouter(
    prefix="/stress",
    tags=["stress"]
)

# Shared service instance
service = StressService()

@router.post("", response_model=StressResponse, status_code=status.HTTP_200_OK)
@router.post("/analyze", response_model=StressResponse, status_code=status.HTTP_200_OK)
async def analyze_stress(payload: StressInput):
    """
    Analyzes user financial indicators, detects risk factors, and computes the stress score.
    Supports both POST /stress and POST /stress/analyze.
    """
    try:
        return service.analyze_stress(payload)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Financial Stress Score analysis failed: {e}"
        )

@router.get("/summary", response_model=SummaryResponse, status_code=status.HTTP_200_OK)
@router.get("", response_model=Any, status_code=status.HTTP_200_OK)
async def get_stress_summary(
    user_id: str = Query(..., min_length=1, description="Unique user identifier")
):
    """
    Generates a dashboard-ready visualization summary containing the latest gauge score, trend, and level.
    Supports both GET /stress/summary and GET /stress.
    """
    history = service.get_history(user_id)
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
        
        # A higher score represents a healthier/more stable state (improving)
        if latest_score > prev_score:
            trend = "Improving"
        elif latest_score < prev_score:
            trend = "Declining"
        else:
            trend = "Stable"
    else:
        trend = "Stable"
        
    return SummaryResponse(
        gauge_score=latest["stress_score"],
        trend=trend,
        stress_level=latest["stress_level"]
    )

@router.get("/history", status_code=status.HTTP_200_OK)
async def get_stress_history(
    user_id: str = Query(..., min_length=1, description="Unique user identifier")
):
    """
    Retrieves the chronological history of past stress evaluations for the specified user.
    """
    history = service.get_history(user_id)
    return {
        "user_id": user_id,
        "history_count": len(history),
        "history": history
    }

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_by_id(id: int):
    """
    Legacy placeholder for get-by-id queries.
    """
    return {"message": f"Get item {id} from stress"}
