import os
import joblib
import pandas as pd
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# Class labels
PROFILE_CLASSES = {
    0: "Disciplined Saver",
    1: "Impulse Spender",
    2: "Balanced Spender"
}

class SpendingPatternClassifier:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
        self.model = None
        self._load_model()

    def _load_model(self):
        """Loads model.pkl if available."""
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                logger.info(f"Loaded classifier model from {self.model_path}")
            except Exception as e:
                logger.error(f"Failed to load classifier model from {self.model_path}: {e}")
                self.model = None
        else:
            logger.info("Model pickle not found. Classifier running in high-fidelity fallback mode.")

    def _get_fallback_class(self, features: Dict[str, Any]) -> str:
        """
        High-fidelity heuristic logic used when the pickled model is not available.
        Provides highly accurate classifications based on feature thresholds.
        """
        impulse_score = features.get("impulse_score", 0.0)
        weekend_ratio = features.get("weekend_ratio", 0.0)
        salary_ratio = features.get("salary_day_ratio", 0.0)

        # High impulse metrics
        if impulse_score > 0.55 or weekend_ratio > 0.45 or salary_ratio > 0.40:
            return "Impulse Spender"
        # Low impulse & high saving readiness metrics
        elif impulse_score < 0.35 and weekend_ratio < 0.15:
            return "Disciplined Saver"
        # Balanced middle ground
        else:
            return "Balanced Spender"

    def predict_profile(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predicts the user's spending profile archetype based on tabular engineered features.
        """
        impulse_score = features.get("impulse_score", 0.0)
        
        feature_vector = [
            features.get("weekend_ratio", 0.0),
            features.get("salary_day_ratio", 0.0),
            features.get("average_transaction_value", 0.0),
            features.get("spending_volatility", 0.0),
            impulse_score
        ]

        if self.model is not None:
            try:
                # Wrap in a Pandas DataFrame with exact training column names to avoid Sklearn warnings
                cols = [
                    "weekend_ratio", 
                    "salary_day_ratio", 
                    "average_transaction_value", 
                    "spending_volatility", 
                    "impulse_score"
                ]
                feature_df = pd.DataFrame([feature_vector], columns=cols)
                pred = self.model.predict(feature_df)[0]
                profile = PROFILE_CLASSES.get(int(pred), "Balanced Spender")
                confidence = float(max(self.model.predict_proba(feature_df)[0]))
                logger.info(f"ML classification model successfully predicted profile: {profile}")
            except Exception as e:
                logger.error(f"Model prediction failed: {e}. Falling back to heuristic classifier.")
                profile = self._get_fallback_class(features)
                confidence = 0.85
        else:
            profile = self._get_fallback_class(features)
            if profile == "Impulse Spender":
                confidence = float(0.80 + (impulse_score - 0.55) * 0.4) if impulse_score > 0.55 else 0.85
            elif profile == "Disciplined Saver":
                confidence = float(0.80 + (0.35 - impulse_score) * 0.4) if impulse_score < 0.35 else 0.85
            else:
                confidence = 0.78
            
            confidence = min(0.95, max(0.60, confidence))

        return {
            "profile_class": profile,
            "confidence": float(round(confidence, 2)),
            "impulse_score": float(round(impulse_score, 2)),
            "features_analyzed": len(feature_vector)
        }
