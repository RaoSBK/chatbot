import os
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def synthesize_dataset(num_samples: int = 300) -> tuple:
    """
    Generates a high-fidelity synthetic dataset representing 5 financial personality archetypes:
      0: Planner
      1: Saver
      2: Impulse Buyer
      3: Explorer
      4: Dreamer
    """
    np.random.seed(42)
    data = []
    
    # Archetype 0: Planner (high budget consistency, high goal commitment, high discipline)
    for _ in range(num_samples // 5):
        savings = np.random.uniform(50.0, 95.0)
        discipline = np.random.uniform(70.0, 95.0)
        goals = np.random.uniform(70.0, 98.0)
        impulse = np.random.uniform(5.0, 30.0)
        stability = np.random.uniform(70.0, 95.0)
        exploration = np.random.uniform(10.0, 45.0)
        budget = np.random.uniform(72.0, 98.0)
        resilience = np.random.uniform(70.0, 95.0)
        data.append([savings, discipline, goals, impulse, stability, exploration, budget, resilience, 0])

    # Archetype 1: Saver (high savings, low exploration, high discipline, moderate-high stability)
    for _ in range(num_samples // 5):
        savings = np.random.uniform(80.0, 100.0)
        discipline = np.random.uniform(75.0, 98.0)
        goals = np.random.uniform(50.0, 85.0)
        impulse = np.random.uniform(0.0, 20.0)
        stability = np.random.uniform(75.0, 98.0)
        exploration = np.random.uniform(0.0, 25.0)
        budget = np.random.uniform(70.0, 95.0)
        resilience = np.random.uniform(75.0, 98.0)
        data.append([savings, discipline, goals, impulse, stability, exploration, budget, resilience, 1])

    # Archetype 2: Impulse Buyer (high impulse, low discipline, low budget consistency, high exploration)
    for _ in range(num_samples // 5):
        savings = np.random.uniform(0.0, 40.0)
        discipline = np.random.uniform(0.0, 45.0)
        goals = np.random.uniform(10.0, 50.0)
        impulse = np.random.uniform(62.0, 100.0)
        stability = np.random.uniform(20.0, 60.0)
        exploration = np.random.uniform(55.0, 100.0)
        budget = np.random.uniform(10.0, 55.0)
        resilience = np.random.uniform(20.0, 60.0)
        data.append([savings, discipline, goals, impulse, stability, exploration, budget, resilience, 2])

    # Archetype 3: Explorer (high exploration, moderate savings, moderate discipline, moderate goals)
    for _ in range(num_samples // 5):
        savings = np.random.uniform(35.0, 70.0)
        discipline = np.random.uniform(45.0, 72.0)
        goals = np.random.uniform(45.0, 75.0)
        impulse = np.random.uniform(30.0, 65.0)
        stability = np.random.uniform(55.0, 85.0)
        exploration = np.random.uniform(65.0, 95.0)
        budget = np.random.uniform(45.0, 75.0)
        resilience = np.random.uniform(55.0, 85.0)
        data.append([savings, discipline, goals, impulse, stability, exploration, budget, resilience, 3])

    # Archetype 4: Dreamer (low-moderate savings, low goal completion [but many goals], low discipline)
    for _ in range(num_samples - 4 * (num_samples // 5)):
        savings = np.random.uniform(20.0, 60.0)
        discipline = np.random.uniform(15.0, 52.0)
        goals = np.random.uniform(10.0, 42.0) # Poor goal completion rate
        impulse = np.random.uniform(40.0, 75.0)
        stability = np.random.uniform(30.0, 68.0)
        exploration = np.random.uniform(35.0, 70.0)
        budget = np.random.uniform(20.0, 58.0)
        resilience = np.random.uniform(30.0, 68.0)
        data.append([savings, discipline, goals, impulse, stability, exploration, budget, resilience, 4])

    cols = [
        "savings_behavior_score",
        "discipline_score",
        "goal_commitment_score",
        "impulse_risk_score",
        "financial_stability_score",
        "exploration_score",
        "budget_consistency_score",
        "stress_resilience_score",
        "label"
    ]
    df = pd.DataFrame(data, columns=cols)
    
    # Shuffle
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    
    X = df.drop("label", axis=1)
    y = df["label"]
    return X, y

def train_model():
    """
    Trains, evaluates, and serializes the RandomForest personality archetype classifier.
    """
    print("Generating synthetic financial personality features...")
    X, y = synthesize_dataset(num_samples=300)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    # Initialize Random Forest Classifier
    print("Training RandomForestClassifier model...")
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
    print(classification_report(y_test, y_pred, target_names=["Planner", "Saver", "Impulse", "Explorer", "Dreamer"]))
    
    # Save the model
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    joblib.dump(clf, model_path)
    print(f"Model successfully saved to {model_path}")

if __name__ == "__main__":
    train_model()
