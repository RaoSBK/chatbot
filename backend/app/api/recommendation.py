from typing import List
from fastapi import APIRouter, Depends, Request, status
from app.schemas.recommendation_schema import RecommendationRequest, RecommendationResponse
from app.services.recommendation_service import RecommendationService
from app.core.limiter import limiter

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.post("", response_model=List[RecommendationResponse], status_code=status.HTTP_200_OK)
@limiter.limit("100/minute")
async def generate_saving_recommendations(
    request: Request,
    payload: RecommendationRequest,
    service: RecommendationService = Depends(RecommendationService)
):
    """
    Analyze spending habits and generate personalized money-saving recommendations.
    """
    return service.generate_recommendations(payload)
