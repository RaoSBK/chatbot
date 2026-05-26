import os
import joblib
import pandas as pd
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Archetype labels matching train.py
ARCHETYPE_LABELS = {
    0: "Planner",
    1: "Saver",
    2: "Impulse Buyer",
    3: "Explorer",
    4: "Dreamer"
}

class FinancialPersonalityClassifier:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
        self.model = None
        self._load_model()

    def _load_model(self):
        """Loads the serialized model.pkl if available."""
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                logger.info(f"Successfully loaded personality classifier from {self.model_path}")
            except Exception as e:
                logger.error(f"Failed to load personality classifier from {self.model_path}: {e}")
                self.model = None
        else:
            logger.info("Pickled personality classifier not found. Operating in fallback rules mode.")

    def predict_archetype(self, features: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Runs ML Random Forest prediction on the engineered feature vector.
        Returns a dictionary with predicted archetype and probability confidence,
        or None if the pickled model is not loaded.
        """
        if self.model is None:
            return None

        # Prepare feature vector matching train.py columns
        cols = [
            "savings_behavior_score",
            "discipline_score",
            "goal_commitment_score",
            "impulse_risk_score",
            "financial_stability_score",
            "exploration_score",
            "budget_consistency_score",
            "stress_resilience_score"
        ]
        
        feature_vector = [features.get(c, 50.0) for c in cols]

        try:
            # Predict using Scikit-Learn RandomForestClassifier
            feature_df = pd.DataFrame([feature_vector], columns=cols)
            pred = self.model.predict(feature_df)[0]
            confidence = float(max(self.model.predict_proba(feature_df)[0]))
            
            profile = ARCHETYPE_LABELS.get(int(pred), "Planner")
            
            return {
                "personality_type": profile,
                "confidence": float(round(confidence, 2))
            }
        except Exception as e:
            logger.error(f"Failed to execute ML prediction: {e}")
            return None
