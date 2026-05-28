from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Dict, Any
from app.schemas.personality_schema import PersonalityInput, PersonalityResponse, DashboardResponse
from app.services.personality_service import PersonalityService

# We use the config-based metadata in ml-engine for dashboard summaries
import os
from app.utils.ml_loader import ml_engine_context
ENGINE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml-engine", "personality-dna-engine"))

router = APIRouter(
    prefix="/personality",
    tags=["personality"]
)

# Shared service instance
service = PersonalityService()

@router.post("", response_model=PersonalityResponse, status_code=status.HTTP_200_OK)
@router.post("/analyze", response_model=PersonalityResponse, status_code=status.HTTP_200_OK)
async def analyze_personality(payload: PersonalityInput):
    """
    Analyzes user financial behavioral metrics and returns the predicted personality profile.
    Supports both POST /personality and POST /personality/analyze.
    """
    try:
        return service.analyze_personality(payload)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Financial Personality DNA analysis failed: {e}"
        )

@router.get("/profile", response_model=DashboardResponse, status_code=status.HTTP_200_OK)
@router.get("", response_model=Any, status_code=status.HTTP_200_OK)
async def get_personality_profile_dashboard(
    user_id: str = Query(..., min_length=1, description="Unique user identifier")
):
    """
    Generates a dashboard-ready financial profile summary containing gauge score and brand color.
    Supports both GET /personality/profile and GET /personality.
    """
    latest = service.get_latest_profile(user_id)
    if not latest:
        raise HTTPException(
            status_code=404,
            detail=f"No personality profile history found for user '{user_id}'."
        )
        
    ptype = latest["personality_type"]
    
    with ml_engine_context(ENGINE_DIR):
        from config import ARCHETYPES_METADATA
        meta = ARCHETYPES_METADATA.get(ptype, ARCHETYPES_METADATA["Planner"])
        
    return DashboardResponse(
        type=ptype,
        confidence=int(round(latest["confidence"] * 100)),
        primary_color=meta["primary_color"],
        summary=meta["summary"]
    )

@router.get("/history", status_code=status.HTTP_200_OK)
async def get_personality_history(
    user_id: str = Query(..., min_length=1, description="Unique user identifier")
):
    """
    Retrieves the chronological history of past personality classifications for the specified user.
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
    return {"message": f"Get item {id} from personality"}
