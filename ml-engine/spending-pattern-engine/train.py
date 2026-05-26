import os
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def synthesize_dataset(num_samples: int = 300) -> tuple:
    """
    Generates a high-fidelity synthetic dataset representing financial behaviors.
    Classes:
      0: Disciplined Saver
      1: Impulse Spender
      2: Balanced Spender
    """
    np.random.seed(42)
    data = []
    
    # 1. Generate Disciplined Savers (Class 0)
    for _ in range(num_samples // 3):
        weekend_ratio = np.random.uniform(-0.10, 0.15)
        salary_day_ratio = np.random.uniform(0.05, 0.18)
        avg_tx = np.random.uniform(100.0, 450.0)
        volatility = np.random.uniform(50.0, 300.0)
        impulse_score = np.random.uniform(0.05, 0.28)
        data.append([weekend_ratio, salary_day_ratio, avg_tx, volatility, impulse_score, 0])
        
    # 2. Generate Impulse Spenders (Class 1)
    for _ in range(num_samples // 3):
        weekend_ratio = np.random.uniform(0.35, 1.20)
        salary_day_ratio = np.random.uniform(0.35, 0.70)
        avg_tx = np.random.uniform(600.0, 2500.0)
        volatility = np.random.uniform(1000.0, 3500.0)
        impulse_score = np.random.uniform(0.58, 0.95)
        data.append([weekend_ratio, salary_day_ratio, avg_tx, volatility, impulse_score, 1])

    # 3. Generate Balanced Spenders (Class 2)
    for _ in range(num_samples - 2 * (num_samples // 3)):
        weekend_ratio = np.random.uniform(0.10, 0.35)
        salary_day_ratio = np.random.uniform(0.18, 0.32)
        avg_tx = np.random.uniform(300.0, 800.0)
        volatility = np.random.uniform(300.0, 1000.0)
        impulse_score = np.random.uniform(0.28, 0.58)
        data.append([weekend_ratio, salary_day_ratio, avg_tx, volatility, impulse_score, 2])

    columns = [
        "weekend_ratio", 
        "salary_day_ratio", 
        "average_transaction_value", 
        "spending_volatility", 
        "impulse_score", 
        "label"
    ]
    df = pd.DataFrame(data, columns=columns)
    
    # Shuffle
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    
    X = df.drop("label", axis=1)
    y = df["label"]
    return X, y

def train_model():
    """
    Trains, evaluates, and serializes the RandomForest spending pattern classifier.
    """
    print("Generating synthetic financial transaction features...")
    X, y = synthesize_dataset(num_samples=300)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    # Initialize Random Forest Classifier
    print("Training RandomForest model...")
    clf = RandomForestClassifier(
        n_estimators=100, 
        max_depth=6, 
        random_state=42, 
        class_weight="balanced"
    )
    clf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy on test split: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Saver", "Impulse", "Balanced"]))
    
    # Save the model
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    joblib.dump(clf, model_path)
    print(f"Model successfully saved to {model_path}")

if __name__ == "__main__":
    train_model()
