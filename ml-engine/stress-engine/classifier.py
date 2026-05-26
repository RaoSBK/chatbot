import os
import joblib
import pandas as pd
import logging
from typing import Dict, Any

from scoring import calculate_weighted_score

logger = logging.getLogger(__name__)

class FinancialStressClassifier:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
        self.model = None
        self._load_model()

    def _load_model(self):
        """Loads model.pkl if available."""
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                logger.info(f"Loaded stress regressor model from {self.model_path}")
            except Exception as e:
                logger.error(f"Failed to load stress regressor model from {self.model_path}: {e}")
                self.model = None
        else:
            logger.info("Stress regressor model not found. Classifier running in math fallback mode.")

    def predict_score(self, features: Dict[str, Any]) -> float:
        """
        Predicts the financial stress score (0-100) using ML regression.
        Falls back to math scoring if model is unavailable.
        """
        # Vector order matching the model training columns
        cols = [
            "savings_rate",
            "budget_pressure",
            "volatility_index",
            "goal_health_score",
            "impulse_risk",
            "weekend_risk",
            "subscription_burden",
            "category_risk"
        ]
        
        feature_vector = [features.get(c, 0.0) for c in cols]

        if self.model is not None:
            try:
                # Predict score via RandomForestRegressor
                feature_df = pd.DataFrame([feature_vector], columns=cols)
                score = float(self.model.predict(feature_df)[0])
                logger.info(f"ML regression model successfully predicted stress score: {score:.2f}")
                return max(0.0, min(100.0, score))
            except Exception as e:
                logger.error(f"Model prediction failed: {e}. Falling back to mathematical scorer.")
                return calculate_weighted_score(features)
        else:
            return calculate_weighted_score(features)
