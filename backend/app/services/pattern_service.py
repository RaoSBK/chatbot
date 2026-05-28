import os
from typing import Dict, Any, List, Optional
from app.utils.ml_loader import ml_engine_context
from app.schemas.patterns_schema import AnalyzeRequest

ENGINE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml-engine", "spending-pattern-engine"))

# In-memory history tracking
ANALYSIS_HISTORY: Dict[str, List[Dict[str, Any]]] = {}

class PatternService:
    def __init__(self):
        # We will instantiate the classifier inside the context when needed,
        # or load it dynamically to keep the context clean.
        pass

    def analyze_patterns(self, payload: AnalyzeRequest) -> Dict[str, Any]:
        """
        Parses transaction history, extracts features, detects patterns,
        and classifies spending profile using ML spending pattern classifier.
        """
        user_id = payload.user_id
        raw_txs = [tx.model_dump() for tx in payload.transactions]
        
        with ml_engine_context(ENGINE_DIR):
            from feature_engineering import engineer_features
            from pattern_detector import detect_patterns
            from classifier import SpendingPatternClassifier
            from insight_generator import generate_insights
            
            features = engineer_features(raw_txs)
            patterns = detect_patterns(raw_txs, features)
            
            # Instantiate classifier in context
            classifier = SpendingPatternClassifier()
            profile_data = classifier.predict_profile(features)
            
            full_insights = generate_insights(patterns, profile_data)
            
        # Store in history (max 5 records)
        if user_id not in ANALYSIS_HISTORY:
            ANALYSIS_HISTORY[user_id] = []
        ANALYSIS_HISTORY[user_id].append(full_insights)
        if len(ANALYSIS_HISTORY[user_id]) > 5:
            ANALYSIS_HISTORY[user_id].pop(0)
            
        return {
            "patterns": patterns,
            "full_insights": full_insights
        }

    def get_latest_analysis(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the latest analysis insights for the user.
        """
        history = ANALYSIS_HISTORY.get(user_id, [])
        return history[-1] if history else None

    def get_history(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves the pattern analysis history for the user.
        """
        return ANALYSIS_HISTORY.get(user_id, [])
