from fastapi import APIRouter, Depends, Request, status
from app.schemas.investment_schema import ChatRequest, ChatResponse
from app.services.investment_assistant_service import InvestmentAssistantService
from app.core.limiter import limiter

router = APIRouter(prefix="/investment-assistant", tags=["investment-assistant"])

@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
@limiter.limit("60/minute")
async def chat_with_assistant(
    request: Request,
    payload: ChatRequest,
    service: InvestmentAssistantService = Depends(InvestmentAssistantService)
):
    """
    Chat with the AI Investment Education Assistant to learn personal finance concepts.
    This assistant is strictly educational and never provides direct investment advice.
    """
    return await service.get_response(payload)
