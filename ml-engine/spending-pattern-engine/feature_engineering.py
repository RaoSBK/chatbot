import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any

from config import (
    LATE_NIGHT_START_HOUR,
    LATE_NIGHT_END_HOUR,
    WEIGHT_LATE_NIGHT,
    WEIGHT_FREQUENCY_BURST,
    WEIGHT_DISCRETIONARY_RATIO
)

def engineer_features(transactions: List[Dict[str, Any]], monthly_income: float = 30000.0) -> Dict[str, Any]:
    """
    Parses transaction history and engineers a robust tabular feature vector for rule-based
    and ML pattern classification.
    """
    # Safeguard empty transactions list
    if not transactions:
        return {
            "daily_spending": 0.0,
            "weekly_spending": 0.0,
            "monthly_spending": 0.0,
            "weekend_ratio": 0.0,
            "salary_day_ratio": 0.0,
            "category_distribution": {},
            "average_transaction_value": 0.0,
            "transaction_frequency": 0.0,
            "subscription_count": 0,
            "spending_volatility": 0.0,
            "impulse_score": 0.0
        }

    # Convert to DataFrame
    df = pd.DataFrame(transactions)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    df["date"] = pd.to_datetime(df["date"])
    
    # Sort chronologically
    df = df.sort_values("date").reset_index(drop=True)
    
    # Time delta
    min_date = df["date"].min()
    max_date = df["date"].max()
    total_days = max(1, (max_date - min_date).days + 1)
    total_months = max(1, total_days / 30.0)

    # Core Aggregates
    total_spending = df["amount"].sum()
    daily_spending = float(total_spending / total_days)
    weekly_spending = float(daily_spending * 7)
    monthly_spending = float(total_spending / total_months)
    average_transaction_value = float(df["amount"].mean())
    transaction_frequency = float(len(df) / total_days)

    # Weekend vs Weekday analysis
    # Weekday mapping: 5=Saturday, 6=Sunday
    df["is_weekend"] = df["date"].dt.weekday.isin([5, 6])
    weekend_spend = df[df["is_weekend"]]["amount"].sum()
    weekday_spend = df[~df["is_weekend"]]["amount"].sum()
    
    weekend_days = df[df["is_weekend"]]["date"].nunique()
    weekday_days = df[~df["is_weekend"]]["date"].nunique()
    
    # Normalize to get average daily spend per weekend vs weekday
    avg_weekend_daily = float(weekend_spend / weekend_days) if weekend_days > 0 else 0.0
    avg_weekday_daily = float(weekday_spend / weekday_days) if weekday_days > 0 else 0.0
    
    # Ratio: how much more is spent on a weekend day vs a weekday day
    if avg_weekday_daily > 0:
        weekend_ratio = float((avg_weekend_daily - avg_weekday_daily) / avg_weekday_daily)
    else:
        weekend_ratio = 0.0

    # Salary-day analysis (assumes salary is on the 1st of every month, checking days 1, 2, 3, 4, 5)
    df["day_of_month"] = df["date"].dt.day
    salary_window_spend = df[df["day_of_month"].between(1, 5)]["amount"].sum()
    salary_day_ratio = float(salary_window_spend / total_spending) if total_spending > 0 else 0.0

    # Category distribution
    cat_distribution = df.groupby("category")["amount"].sum().to_dict()
    # Normalize to ratios
    category_distribution = {cat: float(val / total_spending) for cat, val in cat_distribution.items()} if total_spending > 0 else {}

    # Spending Volatility (std of daily spend)
    daily_series = df.groupby(df["date"].dt.date)["amount"].sum()
    # Fill missing dates in index to get true volatility
    all_dates = pd.date_range(start=min_date, end=max_date, freq="D")
    daily_series = daily_series.reindex(all_dates.date, fill_value=0.0)
    spending_volatility = float(daily_series.std()) if len(daily_series) > 1 else 0.0

    # Subscription Detection (detect same description and amount repeats monthly)
    # E.g. Group by description and amount and check frequency
    sub_count = 0
    grouped_subs = df.groupby(["description", "amount"])
    for (desc, amt), grp in grouped_subs:
        desc_lower = str(desc).lower()
        # Direct keyword match for popular subscriptions
        is_sub_keyword = any(kw in desc_lower for kw in ["netflix", "spotify", "prime", "youtube", "icloud", "microsoft", "gym"])
        if len(grp) >= 2:
            # Check time intervals between transactions to ensure they are ~30 days apart
            grp = grp.sort_values("date")
            intervals = grp["date"].diff().dt.days.dropna()
            if len(intervals) > 0 and all(27 <= x <= 32 for x in intervals):
                sub_count += 1
            elif is_sub_keyword:
                sub_count += 1
        elif is_sub_keyword:
            sub_count += 1

    # Impulse Spending Indicator calculations:
    # 1. Late-night ratio
    # Parse transaction description / time if available. If time not provided, simulate based on description
    # Let's check if 'time' field exists. If not, check description for late-night cues or simulate
    df["hour"] = df["date"].dt.hour
    # If all hours are zero (i.e. only dates were passed), we check late-night keywords or simulate a reasonable ratio
    has_time = df["hour"].nunique() > 1
    if has_time:
        late_night_txs = df[df["hour"].between(LATE_NIGHT_START_HOUR, 23) | df["hour"].between(0, LATE_NIGHT_END_HOUR)]
        late_night_ratio = len(late_night_txs) / len(df)
    else:
        # Check description keywords for late-night activities (e.g. pub, bar, delivery, fast food, uber, cab)
        late_night_keywords = ["delivery", "swiggy", "zomato", "uber", "cab", "bar", "pub", "club", "party"]
        match_count = df["description"].str.lower().apply(lambda d: any(kw in str(d) for kw in late_night_keywords)).sum()
        late_night_ratio = float(match_count / len(df))

    # 2. Time-burst frequency (multiple purchases on same day within short period)
    same_day_counts = df.groupby(df["date"].dt.date).size()
    burst_days = same_day_counts[same_day_counts >= 3]
    frequency_burst_score = float(len(burst_days) / total_days)

    # 3. Discretionary ratio (Discretionary categories over total spending)
    discretionary_categories = ["food", "dining", "entertainment", "leisure", "shopping", "apparel"]
    discretionary_spend = 0.0
    for cat, amount in cat_distribution.items():
        if cat.lower() in discretionary_categories:
            discretionary_spend += float(amount)
    discretionary_ratio = float(discretionary_spend / total_spending) if total_spending > 0 else 0.0

    # Normalize components to [0.0, 1.0] and compute weighted impulse score
    norm_late_night = min(1.0, late_night_ratio / 0.20)
    norm_burst = min(1.0, frequency_burst_score / 0.15)
    norm_discretionary = min(1.0, discretionary_ratio / 0.50)

    impulse_score = float(
        WEIGHT_LATE_NIGHT * norm_late_night +
        WEIGHT_FREQUENCY_BURST * norm_burst +
        WEIGHT_DISCRETIONARY_RATIO * norm_discretionary
    )

    return {
        "daily_spending": float(daily_spending),
        "weekly_spending": float(weekly_spending),
        "monthly_spending": float(monthly_spending),
        "weekend_ratio": float(weekend_ratio),
        "salary_day_ratio": float(salary_day_ratio),
        "category_distribution": category_distribution,
        "average_transaction_value": float(average_transaction_value),
        "transaction_frequency": float(transaction_frequency),
        "subscription_count": int(sub_count),
        "spending_volatility": float(spending_volatility),
        "impulse_score": float(impulse_score)
    }
