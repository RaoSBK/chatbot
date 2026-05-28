from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Dict, Any
from app.schemas.patterns_schema import AnalyzeRequest, AnalyzeResponse, PatternResponse, PatternsSummaryResponse
from app.services.pattern_service import PatternService

router = APIRouter(
    prefix="/patterns",
    tags=["patterns"]
)

# Shared service instance
service = PatternService()

@router.post("/analyze", response_model=AnalyzeResponse, status_code=status.HTTP_200_OK)
async def analyze_patterns(payload: AnalyzeRequest):
    """
    Parses transaction history, extracts engineered features, executes rules,
    runs the ML profile classifier, and returns structured spending patterns.
    """
    if not payload.transactions:
        raise HTTPException(
            status_code=400,
            detail="Cannot analyze empty transaction log."
        )
    try:
        result = service.analyze_patterns(payload)
        patterns = result["patterns"]
        return AnalyzeResponse(patterns=[PatternResponse(**p) for p in patterns])
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Spending Pattern analysis failed: {e}"
        )

@router.get("/summary", response_model=PatternsSummaryResponse, status_code=status.HTTP_200_OK)
async def get_patterns_summary(
    user_id: str = Query(..., min_length=1, description="Unique user identifier")
):
    """
    Generates a high-level coaching summary for the user based on their latest analysis.
    """
    latest = service.get_latest_analysis(user_id)
    if not latest:
        return PatternsSummaryResponse(
            user_id=user_id,
            profile="Unknown",
            impulse_score=0.0,
            total_patterns_detected=0,
            high_severity_alerts=[],
            medium_severity_alerts=[],
            summary_statement="No history found. Call /patterns/analyze first."
        )

    patterns = latest.get("patterns", [])
    classification = latest.get("classification", {})
    
    high_severity_patterns = [p["pattern_type"] for p in patterns if p["severity"] == "High"]
    medium_severity_patterns = [p["pattern_type"] for p in patterns if p["severity"] == "Medium"]

    return PatternsSummaryResponse(
        user_id=user_id,
        profile=classification.get("profile_class", "Balanced Spender"),
        impulse_score=classification.get("impulse_score", 0.0),
        total_patterns_detected=len(patterns),
        high_severity_alerts=high_severity_patterns,
        medium_severity_alerts=medium_severity_patterns,
        summary_statement=f"User is classified as a {classification.get('profile_class')} with {len(high_severity_patterns)} critical alerts."
    )

@router.get("/history", status_code=status.HTTP_200_OK)
async def get_patterns_history(
    user_id: str = Query(..., min_length=1, description="Unique user identifier")
):
    """
    Retrieves the chronological history of past pattern analyses for the specified user.
    """
    history = service.get_history(user_id)
    return {
        "user_id": user_id,
        "history_count": len(history),
        "history": history
    }
