import os
from typing import Dict, Any, List, Optional
from app.utils.ml_loader import ml_engine_context
from app.schemas.personality_schema import PersonalityInput

ENGINE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml-engine", "personality-dna-engine"))

# In-memory history tracking (session_id or user_id -> List of past reports)
PERSONALITY_HISTORY: Dict[str, List[Dict[str, Any]]] = {}

class PersonalityService:
    def __init__(self):
        pass

    def analyze_personality(self, payload: PersonalityInput) -> Dict[str, Any]:
        """
        Runs the feature engineering and ensemble ML decision layer in-process.
        """
        user_id = payload.user_id or "default_user"
        raw_data = payload.model_dump()
        
        with ml_engine_context(ENGINE_DIR):
            from feature_engineering import engineer_features
            from ensemble_model import get_personality_profile
            
            features = engineer_features(raw_data)
            profile = get_personality_profile(raw_data, features)
            
        # Store in history (max 5 records)
        if user_id not in PERSONALITY_HISTORY:
            PERSONALITY_HISTORY[user_id] = []
        PERSONALITY_HISTORY[user_id].append(profile)
        if len(PERSONALITY_HISTORY[user_id]) > 5:
            PERSONALITY_HISTORY[user_id].pop(0)
            
        return profile

    def get_latest_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the latest analyzed profile for the user.
        """
        history = PERSONALITY_HISTORY.get(user_id, [])
        return history[-1] if history else None

    def get_history(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves the analysis history for the user.
        """
        return PERSONALITY_HISTORY.get(user_id, [])
