import pandas as pd
import numpy as np
from typing import List, Dict, Any
from datetime import datetime

from config import (
    WEEKEND_OVERSPEND_THRESHOLD,
    SALARY_SPIKE_RATIO_THRESHOLD,
    CATEGORY_SPIKE_THRESHOLD,
    ANOMALY_Z_SCORE_THRESHOLD
)

def detect_patterns(transactions: List[Dict[str, Any]], features: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Analyzes transaction records and engineered features to isolate 7 core spending patterns
    with severity ratings, confidence metrics, and human-scannable descriptions.
    """
    patterns = []
    
    if not transactions:
        return patterns

    df = pd.DataFrame(transactions)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    df["date"] = pd.to_datetime(df["date"])
    
    # Chronological sort
    df = df.sort_values("date").reset_index(drop=True)
    
    total_spending = df["amount"].sum()
    if total_spending <= 0:
        return patterns

    # Extract time metrics
    min_date = df["date"].min()
    max_date = df["date"].max()
    total_days = max(1, (max_date - min_date).days + 1)
    
    # ----------------------------------------------------
    # 1. Weekend Overspending
    # ----------------------------------------------------
    weekend_ratio = features.get("weekend_ratio", 0.0)
    if weekend_ratio > WEEKEND_OVERSPEND_THRESHOLD:
        severity = "High" if weekend_ratio > 0.40 else "Medium"
        confidence = float(min(0.95, 0.75 + (weekend_ratio - WEEKEND_OVERSPEND_THRESHOLD) * 0.4))
        percent = int(round(weekend_ratio * 100))
        patterns.append({
            "pattern_type": "Weekend Overspending",
            "severity": severity,
            "confidence": float(round(confidence, 2)),
            "description": f"User spends {percent}% more on weekends."
        })

    # ----------------------------------------------------
    # 2. Salary-Day Spending Spike
    # ----------------------------------------------------
    salary_day_ratio = features.get("salary_day_ratio", 0.0)
    if salary_day_ratio > SALARY_SPIKE_RATIO_THRESHOLD:
        severity = "High" if salary_day_ratio > 0.35 else "Medium"
        confidence = float(min(0.95, 0.80 + (salary_day_ratio - SALARY_SPIKE_RATIO_THRESHOLD) * 0.5))
        percent = int(round(salary_day_ratio * 100))
        patterns.append({
            "pattern_type": "Salary-Day Spending Spike",
            "severity": severity,
            "confidence": float(round(confidence, 2)),
            "description": f"{percent}% of monthly spending occurs within first 5 days."
        })

    # ----------------------------------------------------
    # 3. Category Spending Spike
    # ----------------------------------------------------
    df["year_month"] = df["date"].dt.to_period("M")
    unique_months = df["year_month"].unique()
    
    if len(unique_months) >= 2:
        latest_month = unique_months[-1]
        historical_months = unique_months[:-1]
        
        latest_df = df[df["year_month"] == latest_month]
        historical_df = df[df["year_month"].isin(historical_months)]
        
        latest_cat = latest_df.groupby("category")["amount"].sum()
        
        hist_cat_total = historical_df.groupby(["year_month", "category"])["amount"].sum().reset_index()
        hist_cat_avg = hist_cat_total.groupby("category")["amount"].mean()
        
        for cat, latest_amount in latest_cat.items():
            hist_avg = hist_cat_avg.get(cat, 0.0)
            if hist_avg > 0:
                increase_ratio = float((latest_amount - hist_avg) / hist_avg)
                if increase_ratio > CATEGORY_SPIKE_THRESHOLD:
                    severity = "High" if increase_ratio > 0.50 else "Medium"
                    confidence = float(min(0.95, 0.70 + increase_ratio * 0.3))
                    percent = int(round(increase_ratio * 100))
                    patterns.append({
                        "pattern_type": "Category Spending Spike",
                        "severity": severity,
                        "confidence": float(round(confidence, 2)),
                        "description": f"{cat} increased {percent}% compared to previous month."
                    })
            elif latest_amount > 500.0:
                patterns.append({
                    "pattern_type": "Category Spending Spike",
                    "severity": "Medium",
                    "confidence": 0.80,
                    "description": f"New elevated spending detected in {cat}."
                })

    # ----------------------------------------------------
    # 4. Subscription Detection
    # ----------------------------------------------------
    sub_count = features.get("subscription_count", 0)
    if sub_count > 0:
        patterns.append({
            "pattern_type": "Subscription Detection",
            "severity": "Low",
            "confidence": 0.95,
            "description": f"Detected {sub_count} active subscriptions."
        })

    # ----------------------------------------------------
    # 5. Unusual Expense Detection (Anomaly Checking)
    # ----------------------------------------------------
    avg_tx = features.get("average_transaction_value", 0.0)
    std_tx = df["amount"].std() if len(df) > 1 else 0.0
    
    anomalies = []
    for idx, row in df.iterrows():
        amt = float(row["amount"])
        # Check Z-score
        if std_tx > 0:
            z_score = (amt - avg_tx) / std_tx
            if z_score > 1.8:  # Modified slightly to handle high-variance subsets
                anomalies.append((amt, z_score))
        # Fallback ratio trigger for spike detection in highly volatile profiles
        if avg_tx > 0 and amt > avg_tx * 2.0:
            ratio = amt / avg_tx
            anomalies.append((amt, ratio))
            
    if anomalies:
        anomalies.sort(key=lambda x: x[0], reverse=True)
        largest_amt, index_val = anomalies[0]
        if avg_tx > 0:
            exceeds_pct = int(round(((largest_amt - avg_tx) / avg_tx) * 100))
        else:
            exceeds_pct = 300
            
        patterns.append({
            "pattern_type": "Unusual Expense Detection",
            "severity": "High" if exceeds_pct > 150 else "Medium",
            "confidence": 0.88,
            "description": f"₹{int(largest_amt)} purchase exceeds typical spending by {exceeds_pct}%."
        })

    # ----------------------------------------------------
    # 6. Spending Trend Analysis
    # ----------------------------------------------------
    monthly_series = df.groupby("year_month")["amount"].sum()
    if len(monthly_series) >= 2:
        recent_months = monthly_series.tail(3)
        pct_change = float((recent_months.iloc[-1] - recent_months.iloc[0]) / recent_months.iloc[0]) if recent_months.iloc[0] > 0 else 0.0
        
        percent = int(round(pct_change * 100))
        if abs(pct_change) > 0.05:
            trend_desc = "increased" if pct_change > 0 else "decreased"
            severity = "High" if (pct_change > 0.20) else "Medium" if (pct_change > 0.10 or pct_change < -0.10) else "Low"
            patterns.append({
                "pattern_type": "Spending Trend Analysis",
                "severity": severity,
                "confidence": 0.85,
                "description": f"Monthly spending {trend_desc} {abs(percent)}% over last 3 months."
            })
        else:
            patterns.append({
                "pattern_type": "Spending Trend Analysis",
                "severity": "Low",
                "confidence": 0.80,
                "description": "Monthly spending is stable over the last 3 months."
            })

    # ----------------------------------------------------
    # 7. Impulse Spending Indicators
    # ----------------------------------------------------
    impulse_score = features.get("impulse_score", 0.0)
    if impulse_score > 0.40:
        severity = "High" if impulse_score > 0.65 else "Medium"
        patterns.append({
            "pattern_type": "Impulse Spending Indicators",
            "severity": severity,
            "confidence": 0.89,
            "description": "Frequent late-night purchases suggest impulse spending."
        })

    return patterns
