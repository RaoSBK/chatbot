import logging
from decimal import Decimal
from typing import List, Dict
from app.schemas.recommendation_schema import RecommendationRequest, RecommendationResponse

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self):
        pass

    def generate_recommendations(self, request: RecommendationRequest) -> List[RecommendationResponse]:
        """
        Analyzes spending category distribution, detects unnecessary or excessive spending,
        calculates possible monthly savings, and generates actionable recommendations with severity,
        confidence, and explanation.
        """
        income = request.monthly_income
        expenses = request.expenses

        if not expenses:
            logger.info("No expenses provided. Skipping recommendations.")
            return []

        # 1. Analyze spending by category
        category_totals: Dict[str, Decimal] = {}
        total_expenses = Decimal("0.0")

        for exp in expenses:
            category = exp.category.strip().title()
            category_totals[category] = category_totals.get(category, Decimal("0.0")) + exp.amount
            total_expenses += exp.amount

        recommendations: List[RecommendationResponse] = []

        # Helper to retrieve total spending across a set of matching category keywords
        def find_category_total(keywords: List[str]) -> Decimal:
            total = Decimal("0.0")
            for cat, amount in category_totals.items():
                if any(kw in cat.lower() for kw in keywords):
                    total += amount
            return total

        # Rule 1: Food Spending Heuristic
        # Matches: food, dining, restaurant, cafe, delivery, groceries
        food_keywords = ["food", "dining", "restaurant", "cafe", "delivery", "groceries", "grocer"]
        food_total = find_category_total(food_keywords)
        if food_total > 0:
            percentage_of_expenses = (food_total / total_expenses) if total_expenses > 0 else Decimal("0.0")
            percentage_of_income = (food_total / income)

            if percentage_of_expenses > Decimal("0.35") or percentage_of_income > Decimal("0.20"):
                severity = "High" if (percentage_of_expenses > Decimal("0.35") or percentage_of_income > Decimal("0.25")) else "Medium"
                possible_savings = (food_total * Decimal("0.20")).quantize(Decimal("0.01"))
                
                reason_str = "Food spending exceeds 35% of total expenses" if percentage_of_expenses > Decimal("0.35") else f"Food spending is high, exceeding {int(percentage_of_income * 100)}% of your monthly income"
                
                recommendations.append(RecommendationResponse(
                    recommendation_type="Food Spending",
                    severity=severity,
                    possible_savings=possible_savings,
                    confidence=0.92,
                    recommendation="Reduce food delivery spending by 20%",
                    reason=reason_str
                ))

        # Rule 2: Entertainment & Leisure Heuristic
        # Matches: entertainment, leisure, movie, game, hobby, fun, cinema, bar, pub, concert
        ent_keywords = ["entertainment", "leisure", "movie", "game", "hobby", "fun", "cinema", "bar", "pub", "concert", "play"]
        ent_total = find_category_total(ent_keywords)
        if ent_total > 0:
            percentage_of_income = ent_total / income
            percentage_of_expenses = ent_total / total_expenses if total_expenses > 0 else Decimal("0.0")
            if percentage_of_income > Decimal("0.10") or percentage_of_expenses > Decimal("0.15"):
                severity = "High" if percentage_of_income > Decimal("0.15") else "Medium"
                possible_savings = (ent_total * Decimal("0.30")).quantize(Decimal("0.01"))
                
                recommendations.append(RecommendationResponse(
                    recommendation_type="Entertainment Spending",
                    severity=severity,
                    possible_savings=possible_savings,
                    confidence=0.85,
                    recommendation="Trim entertainment and leisure expenses by 30%",
                    reason=f"Entertainment spending represents {int(percentage_of_income * 100)}% of your monthly income"
                ))

        # Rule 3: Subscriptions Heuristic
        # Matches: subscription, recurring, streaming, netflix, spotify, premium, membership, gym
        sub_keywords = ["subscription", "recurring", "streaming", "netflix", "spotify", "premium", "membership", "gym", "cloud", "saas"]
        sub_total = find_category_total(sub_keywords)
        if sub_total > 0:
            percentage_of_income = sub_total / income
            if percentage_of_income > Decimal("0.05"):
                possible_savings = (sub_total * Decimal("0.40")).quantize(Decimal("0.01"))
                
                recommendations.append(RecommendationResponse(
                    recommendation_type="Subscription Auditing",
                    severity="Medium",
                    possible_savings=possible_savings,
                    confidence=0.88,
                    recommendation="Audit and cancel unused streaming or app subscriptions",
                    reason=f"Subscription spending is higher than the recommended 5% threshold of monthly income"
                ))

        # Rule 4: Transport Spending Heuristic
        # Matches: transport, travel, ride, uber, taxi, commute, fuel, gas
        trans_keywords = ["transport", "travel", "ride", "uber", "taxi", "commute", "fuel", "gas"]
        trans_total = find_category_total(trans_keywords)
        if trans_total > 0:
            percentage_of_income = trans_total / income
            if percentage_of_income > Decimal("0.15"):
                possible_savings = (trans_total * Decimal("0.15")).quantize(Decimal("0.01"))
                
                recommendations.append(RecommendationResponse(
                    recommendation_type="Transportation Costs",
                    severity="Medium",
                    possible_savings=possible_savings,
                    confidence=0.80,
                    recommendation="Optimize commuting costs by utilizing public transit or carpooling",
                    reason=f"Transportation expenses exceed 15% of monthly income"
                ))

        # Rule 5: Shopping & Apparel Heuristic
        # Matches: shopping, clothes, apparel, luxury, gift, shoes
        shop_keywords = ["shopping", "clothes", "apparel", "luxury", "gift", "shoes", "mall"]
        shop_total = find_category_total(shop_keywords)
        if shop_total > 0:
            percentage_of_income = shop_total / income
            if percentage_of_income > Decimal("0.15"):
                possible_savings = (shop_total * Decimal("0.25")).quantize(Decimal("0.01"))
                
                recommendations.append(RecommendationResponse(
                    recommendation_type="Shopping Spending",
                    severity="Medium",
                    possible_savings=possible_savings,
                    confidence=0.87,
                    recommendation="Defer non-essential shopping and establish a 48-hour cooling-off rule for impulse purchases",
                    reason=f"Shopping spending is elevated, consuming {int(percentage_of_income * 100)}% of your monthly income"
                ))

        # Rule 6: General Savings Rate Heuristic
        if total_expenses > income * Decimal("0.90"):
            possible_savings = (total_expenses - income * Decimal("0.80")).quantize(Decimal("0.01"))
            if possible_savings > 0:
                recommendations.append(RecommendationResponse(
                    recommendation_type="Savings Rate Boost",
                    severity="High",
                    possible_savings=possible_savings,
                    confidence=0.95,
                    recommendation="Create a strict 50/30/20 budget framework to increase your savings rate",
                    reason="Total monthly expenses exceed 90% of your income, leaving less than a 10% savings buffer"
                ))

        # Sort recommendations: High severity first, then Medium, then Low; and sub-sort by possible savings descending
        severity_weight = {"High": 3, "Medium": 2, "Low": 1}
        recommendations.sort(key=lambda r: (severity_weight[r.severity], r.possible_savings), reverse=True)

        logger.info(f"Generated {len(recommendations)} recommendations for monthly income {income}")
        return recommendations

# Legacy backward-compatibility alias
Recommendation_service = RecommendationService
