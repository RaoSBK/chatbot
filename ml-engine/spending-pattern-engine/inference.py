import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

from feature_engineering import engineer_features
from pattern_detector import detect_patterns
from classifier import SpendingPatternClassifier
from insight_generator import generate_insights

app = FastAPI(
    title="MoneyMind X Spending Pattern Detection Microservice",
    description="ML-powered spending pattern analysis, classification, and anomaly detection engine.",
    version="1.0.0"
)

# In-memory database of analysis history (user_id -> List of past insights)
ANALYSIS_HISTORY: Dict[str, List[Dict[str, Any]]] = {}

# Instantiate ML classifier
classifier = SpendingPatternClassifier()

# ----------------------------------------------------
# Pydantic Schemas
# ----------------------------------------------------
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

# ----------------------------------------------------
# API Endpoints
# ----------------------------------------------------
@app.post("/patterns/analyze", response_model=AnalyzeResponse, status_code=status.HTTP_200_OK)
async def analyze_patterns(payload: AnalyzeRequest):
    """
    Parses transaction history, extracts engineered features, executes rules,
    runs the ML profile classifier, and returns structured spending patterns.
    """
    user_id = payload.user_id
    raw_txs = [tx.model_dump() for tx in payload.transactions]
    
    if not raw_txs:
        raise HTTPException(
            status_code=400,
            detail="Cannot analyze empty transaction log."
        )

    # 1. Feature Engineering
    try:
        features = engineer_features(raw_txs)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Feature engineering pipeline failure: {e}"
        )

    # 2. Rule Heuristics
    try:
        patterns = detect_patterns(raw_txs, features)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Pattern detection rule engine failure: {e}"
        )

    # 3. ML Classification Segment
    try:
        profile_data = classifier.predict_profile(features)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ML classification failure: {e}"
        )

    # 4. Synthesize Downstream Insights
    try:
        full_insights = generate_insights(patterns, profile_data)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Insight generation synthesizer failure: {e}"
        )

    # 5. Persist to In-Memory History (max last 5 analyses per user)
    if user_id not in ANALYSIS_HISTORY:
        ANALYSIS_HISTORY[user_id] = []
    
    ANALYSIS_HISTORY[user_id].append(full_insights)
    if len(ANALYSIS_HISTORY[user_id]) > 5:
        ANALYSIS_HISTORY[user_id].pop(0)

    # Expose output in exact required format
    return AnalyzeResponse(patterns=[PatternResponse(**p) for p in patterns])

@app.get("/patterns/history", status_code=status.HTTP_200_OK)
async def get_patterns_history(user_id: str = Query(..., min_length=1, description="Unique user identifier")):
    """
    Retrieves the chronological history of past pattern analyses for the specified user.
    """
    history = ANALYSIS_HISTORY.get(user_id, [])
    return {
        "user_id": user_id,
        "history_count": len(history),
        "history": history
    }

@app.get("/patterns/summary", status_code=status.HTTP_200_OK)
async def get_patterns_summary(user_id: str = Query(..., min_length=1, description="Unique user identifier")):
    """
    Generates a high-level coaching summary for the user based on their latest analysis.
    """
    history = ANALYSIS_HISTORY.get(user_id, [])
    if not history:
        return {
            "user_id": user_id,
            "status": "No history found. Call /patterns/analyze first.",
            "profile": "Unknown",
            "active_patterns": 0,
            "impulse_score": 0.0
        }

    latest = history[-1]
    patterns = latest["patterns"]
    classification = latest["classification"]
    
    high_severity_patterns = [p["pattern_type"] for p in patterns if p["severity"] == "High"]
    medium_severity_patterns = [p["pattern_type"] for p in patterns if p["severity"] == "Medium"]

    return {
        "user_id": user_id,
        "profile": classification.get("profile_class", "Balanced Spender"),
        "impulse_score": classification.get("impulse_score", 0.0),
        "total_patterns_detected": len(patterns),
        "high_severity_alerts": high_severity_patterns,
        "medium_severity_alerts": medium_severity_patterns,
        "summary_statement": f"User is classified as a {classification.get('profile_class')} with {len(high_severity_patterns)} critical alerts."
    }
