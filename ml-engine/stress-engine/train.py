import os
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

from scoring import calculate_weighted_score

def synthesize_dataset(num_samples: int = 350) -> tuple:
    """
    Generates a high-fidelity synthetic dataset representing financial stress behaviors.
    Outputs feature matrix X and target y (stress score 0-100).
    """
    np.random.seed(42)
    features_list = []
    scores_list = []
    
    for _ in range(num_samples):
        # Generate raw-engineered indicators
        savings_rate = np.random.uniform(-0.10, 0.45)
        budget_pressure = np.random.uniform(0.10, 1.20)
        volatility_index = np.random.uniform(0.0, 1.0)
        goal_health_score = np.random.uniform(0.0, 1.0)
        impulse_risk = np.random.uniform(0.0, 1.0)
        # Weekend ratio commonly floats between 0.1 and 2.0
        weekend_risk = np.random.uniform(0.10, 2.0)
        subscription_burden = float(np.random.randint(0, 12))
        category_risk = float(np.random.randint(0, 8))
        
        feats = {
            "savings_rate": savings_rate,
            "budget_pressure": budget_pressure,
            "volatility_index": volatility_index,
            "goal_health_score": goal_health_score,
            "impulse_risk": impulse_risk,
            "weekend_risk": weekend_risk,
            "subscription_burden": subscription_burden,
            "category_risk": category_risk
        }
        
        # Calculate base mathematical score
        base_score = calculate_weighted_score(feats)
        
        # Add random Gaussian noise representing real-world variance (std = 2.0)
        noise = np.random.normal(0.0, 2.0)
        final_score = max(0.0, min(100.0, base_score + noise))
        
        features_list.append([
            savings_rate,
            budget_pressure,
            volatility_index,
            goal_health_score,
            impulse_risk,
            weekend_risk,
            subscription_burden,
            category_risk
        ])
        scores_list.append(final_score)

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
    X = pd.DataFrame(features_list, columns=cols)
    y = pd.Series(scores_list)
    
    return X, y

def train_model():
    """
    Trains, evaluates, and serializes the RandomForest stress score regressor model.
    """
    print("Generating synthetic stress feature vectors...")
    X, y = synthesize_dataset(num_samples=350)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    
    # Initialize Random Forest Regressor
    print("Training RandomForestRegressor model...")
    model = RandomForestRegressor(
        n_estimators=120,
        max_depth=7,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Model Mean Squared Error (MSE): {mse:.4f}")
    print(f"Model R-squared (R2): {r2:.4f}")
    
    # Save the model
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    joblib.dump(model, model_path)
    print(f"Model successfully saved to {model_path}")

if __name__ == "__main__":
    train_model()
