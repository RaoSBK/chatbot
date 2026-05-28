import os
from typing import Dict, Any, List, Optional
from app.utils.ml_loader import ml_engine_context
from app.schemas.stress_schema import StressInput

ENGINE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml-engine", "stress-engine"))

# In-memory history tracking
STRESS_HISTORY: Dict[str, List[Dict[str, Any]]] = {}

class StressService:
    def __init__(self):
        pass

    def analyze_stress(self, payload: StressInput) -> Dict[str, Any]:
        """
        Runs the feature engineering, stress scoring, and ML regressor in-process.
        """
        user_id = payload.user_id or "default_user"
        raw_data = payload.model_dump()
        
        with ml_engine_context(ENGINE_DIR):
            from stress_calculator import evaluate_stress
            report = evaluate_stress(raw_data)
            
        # Store in history (max 5 records)
        if user_id not in STRESS_HISTORY:
            STRESS_HISTORY[user_id] = []
        STRESS_HISTORY[user_id].append(report)
        if len(STRESS_HISTORY[user_id]) > 5:
            STRESS_HISTORY[user_id].pop(0)
            
        return report

    def get_latest_report(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the latest stress evaluation report for the user.
        """
        history = STRESS_HISTORY.get(user_id, [])
        return history[-1] if history else None

    def get_history(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves the chronological stress analysis history for the user.
        """
        return STRESS_HISTORY.get(user_id, [])
