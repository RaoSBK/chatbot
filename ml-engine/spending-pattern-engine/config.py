# Configuration file for Spending Pattern Detection Engine

# Weekend spending over weekdays threshold (e.g., 30% higher)
WEEKEND_OVERSPEND_THRESHOLD = 0.30

# Salary-Day Spending spike threshold (e.g., percentage of monthly spending in first 5 days > 25%)
SALARY_SPIKE_DAYS = 5
SALARY_SPIKE_RATIO_THRESHOLD = 0.25

# Category Spending spike threshold vs historical average (e.g., 40% higher)
CATEGORY_SPIKE_THRESHOLD = 0.40

# Subscription repeat window in days (e.g., 28 to 31 days)
SUBSCRIPTION_WINDOW_MIN = 27
SUBSCRIPTION_WINDOW_MAX = 32

# Z-score threshold for unusual transaction detection (anomalies)
ANOMALY_Z_SCORE_THRESHOLD = 3.0
LARGE_TRANSACTION_THRESHOLD = 5000.0 # Standard high-threshold baseline

# Impulse late-night hour windows
LATE_NIGHT_START_HOUR = 22  # 10 PM
LATE_NIGHT_END_HOUR = 4     # 4 AM

# Weights for calculated Impulse Score
WEIGHT_LATE_NIGHT = 0.30
WEIGHT_FREQUENCY_BURST = 0.30
WEIGHT_DISCRETIONARY_RATIO = 0.40
