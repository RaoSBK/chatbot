from typing import List
from pydantic import BaseModel, Field

class TransactionInput(BaseModel):
    amount: float = Field(..., gt=0.0, description="Amount of the transaction")
    category: str = Field(..., min_length=1, description="Category (e.g., Food, Rent)")
    date: str = Field(..., description="Date of the transaction (YYYY-MM-DD)")
    description: str = Field(..., description="Merchant or description")

class AnalyzeRequest(BaseModel):
    user_id: str = Field(..., min_length=1, description="Unique user identifier")
    transactions: List[TransactionInput] = Field(..., description="List of transactions to analyze")

class PatternResponse(BaseModel):
    pattern_type: str
    severity: str
    confidence: float
    description: str

class AnalyzeResponse(BaseModel):
    patterns: List[PatternResponse]

class PatternsSummaryResponse(BaseModel):
    user_id: str
    profile: str
    impulse_score: float
    total_patterns_detected: int
    high_severity_alerts: List[str]
    medium_severity_alerts: List[str]
    summary_statement: str
