import os
import re
import logging
from typing import Dict, List, Tuple
import google.generativeai as genai

from app.core.config import settings
from app.schemas.investment_schema import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

# Global in-memory memory storage (session_id -> list of (user_msg, assistant_resp) tuples)
# Retains up to the last 5 interactions
CONVERSATION_MEMORY: Dict[str, List[Tuple[str, str]]] = {}

class InvestmentAssistantService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        # Determine if we should run in high-fidelity mock/fallback mode
        self.use_mock = (
            not self.api_key 
            or self.api_key == "your_gemini_api_key_here"
            or os.environ.get("TESTING") == "True"
        )
        if not self.use_mock:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("Gemini API client configured successfully for InvestmentAssistantService.")
            except Exception as e:
                logger.error(f"Failed to configure Gemini API client: {e}. Falling back to mock engine.")
                self.use_mock = True

    def validate_safety(self, text: str) -> bool:
        """
        Validates text against prohibited stock buying advice, direct tips, and guaranteed return claims.
        Returns True if a violation is detected (unsafe).
        """
        text_lower = text.lower()
        
        # 1. Direct explicit phrases
        explicit_blocks = [
            "buy stock", "sell stock", "buy shares", "sell shares", "buy equity", "sell equity",
            "stock recommendation", "stock tip", "stock signal", "buy signal", "sell signal",
            "invest in abc", "invest in xyz", "buy xyz", "buy abc", "sell xyz", "sell abc",
            "financial advice", "investment advice"
        ]
        for phrase in explicit_blocks:
            if phrase in text_lower:
                return True

        # 2. Advice seeking patterns
        advice_triggers = [
            "should i buy", "should i sell", "should i invest", 
            "is it good to buy", "is it good to invest",
            "which stock", "what stock", "recommend stock", "recommend a stock",
            "best stock", "good stock", "top stock", "stocks to buy", "shares to buy",
            "stocks to invest", "invest in a stock", "invest in stocks"
        ]
        for trigger in advice_triggers:
            if trigger in text_lower:
                return True

        # 3. Specific stock ticker or company name coupled with investment intent
        intent_keywords = ["buy", "sell", "invest", "recommend", "stock", "share", "portfolio"]
        banned_entities = [
            "tesla", "apple", "google", "microsoft", "amazon", "nvidia", "meta", "netflix",
            "tsla", "aapl", "msft", "goog", "amzn", "nvda", "xyz", "abc"
        ]
        
        for entity in banned_entities:
            # Word boundary matching to avoid matching substrings like "alphabet"
            if re.search(rf"\b{entity}\b", text_lower):
                # Check if an intent keyword is also present
                if any(intent in text_lower for intent in intent_keywords):
                    return True

        # 4. Guaranteed return or risk-free claims/requests
        guaranteed_keywords = ["guarantee", "risk-free", "risk free", "assured return", "assured profit"]
        return_keywords = ["return", "profit", "yield", "income", "growth", "interest", "double"]
        
        for gk in guaranteed_keywords:
            if gk in text_lower:
                # Allow safe negated/disclaimer sentences like "no guaranteed returns" or "not guaranteed"
                negations = ["no ", "not ", "don't ", "does not ", "never ", "cannot ", "subject to "]
                is_negated = any(neg in text_lower for neg in negations)
                
                # Check if we literally say "no guaranteed return" or "not guaranteed"
                if "no guaranteed return" in text_lower or "not guaranteed" in text_lower:
                    continue
                    
                if not is_negated:
                    return True
                    
                # If it's a question or statement coupling a guarantee with return words, block it
                if any(rk in text_lower for rk in return_keywords):
                    # Direct check for positive claims
                    if not ("does not guarantee" in text_lower or "no guaranteed" in text_lower):
                        return True

        return False

    def _get_mock_response(self, query: str, history: List[Tuple[str, str]]) -> Tuple[str, str]:
        """
        High-fidelity Mock Educational Engine to handle conversations offline or under testing.
        """
        query_lower = query.lower()

        # Handle context/pronouns
        resolved_query = query_lower
        prev_topic = ""
        if history:
            prev_topic = history[-1][0].lower() # Last discussed topic
            if "is it risky" in query_lower or "are they risky" in query_lower:
                resolved_query = f"risks of {prev_topic}"

        # 1. SIP (Systematic Investment Plan)
        if "sip" in resolved_query:
            if "risk" in resolved_query:
                return "SIP", (
                    "Topic:\n"
                    "SIP Risks\n\n"
                    "Explanation:\n"
                    "While SIPs are excellent for compounding, they are not risk-free because they invest in mutual funds, which are tied to equity and bond market movements.\n\n"
                    "Example:\n"
                    "Investing ₹1,000 monthly in an equity fund during a market downturn will buy you more units, but your portfolio value will drop temporarily.\n\n"
                    "Benefits:\n"
                    "- Rupee Cost Averaging (buying more when prices are low, less when prices are high)\n"
                    "- Reduces the pressure of trying to time the market\n\n"
                    "Risks:\n"
                    "- Market Risk (subject to volatility)\n"
                    "- No guaranteed returns (returns depend entirely on fund performance)\n\n"
                    "Takeaway:\n"
                    "SIP risks are reduced over longer durations. Ideal for patient, long-term beginners."
                )
            else:
                return "SIP", (
                    "Topic:\n"
                    "SIP\n\n"
                    "Explanation:\n"
                    "A Systematic Investment Plan (SIP) is a disciplined method of investing a fixed amount of money regularly into a mutual fund rather than a single lump sum.\n\n"
                    "Example:\n"
                    "Setting up an automated transfer of ₹1,000 on the 5th of every month into a mutual fund.\n\n"
                    "Benefits:\n"
                    "- Disciplined investing\n"
                    "- Rupee cost averaging\n\n"
                    "Risks:\n"
                    "- Market fluctuations\n\n"
                    "Takeaway:\n"
                    "Good for beginners who want long-term investing discipline."
                )

        # 2. Compounding
        elif "compound" in resolved_query:
            return "Compounding", (
                "Topic:\n"
                "Compounding\n\n"
                "Explanation:\n"
                "Compounding is the process where your investment's earnings (interest or gains) are reinvested to generate their own earnings over time. It is effectively earning 'interest on interest'.\n\n"
                "Example:\n"
                "If you invest ₹10,000 at a 10% annual interest, you earn ₹1,000 in Year 1. In Year 2, you earn 10% on ₹11,000 (your new balance), which is ₹1,100.\n\n"
                "Benefits:\n"
                "- Generates exponential asset growth over long periods\n"
                "- Strongly rewards early savers\n\n"
                "Risks:\n"
                "- Works in reverse for compound interest on debt (e.g., credit card debt)\n"
                "- Requires significant time to build massive momentum\n\n"
                "Takeaway:\n"
                "Start saving and investing early to give compounding the longest time to grow your wealth."
            )

        # 3. ETF vs Mutual Fund
        elif "etf" in resolved_query or "mutual fund" in resolved_query:
            return "Mutual Funds and ETFs", (
                "Topic:\n"
                "Mutual Funds vs. ETFs\n\n"
                "Explanation:\n"
                "Both options pool money to buy a basket of securities like stocks and bonds. However, active Mutual Funds are managed by professional fund managers and trade once at the end of the day, while ETFs (Exchange-Traded Funds) track an index and trade intraday on exchanges like a stock.\n\n"
                "Example:\n"
                "Investing in an active Large Cap Mutual Fund directly via the fund company vs. buying S&P 500 ETF shares through your trading platform during market hours.\n\n"
                "Benefits:\n"
                "- Offers instant diversification across hundreds of stocks\n"
                "- ETFs generally possess lower management fees than active mutual funds\n\n"
                "Risks:\n"
                "- Active mutual funds can underperform major market indexes\n"
                "- Tracking error in passive ETFs\n\n"
                "Takeaway:\n"
                "ETFs are superb for intraday flexibility and low costs, while Mutual Funds are perfect for fully automated monthly plans."
            )

        # 4. Emergency Fund
        elif "emergency fund" in resolved_query:
            return "Emergency Fund", (
                "Topic:\n"
                "Emergency Funds\n\n"
                "Explanation:\n"
                "An emergency fund is money set aside strictly to cover unplanned expenses (medical bills, job losses, car repair), protecting you from borrowing high-interest loans.\n\n"
                "Example:\n"
                "Maintaining six months of essential living expenses (e.g. ₹1,20,000) in a highly liquid high-yield savings account separate from your spending debit card.\n\n"
                "Benefits:\n"
                "- Safeguards long-term investments from premature liquidations\n"
                "- Provides mental security and a debt-free cushion\n\n"
                "Risks:\n"
                "- Inflation risk (the cash loses purchasing power over long periods compared to stocks)\n\n"
                "Takeaway:\n"
                "A vital first step. Build a liquid reserve of 3 to 6 months of expenses before aggressive investing."
            )

        # 5. Diversification
        elif "diversification" in resolved_query:
            return "Diversification", (
                "Topic:\n"
                "Diversification\n\n"
                "Explanation:\n"
                "Diversification means spreading your money across different investments, sectors, and asset classes to reduce risk. It ensures your portfolio doesn't rely entirely on a single company.\n\n"
                "Example:\n"
                "Rather than putting your entire ₹50,000 savings in a single technology company, you divide it among tech, energy, healthcare, government bonds, and gold.\n\n"
                "Benefits:\n"
                "- Decreases overall portfolio volatility\n"
                "- Protects against total loss if one stock collapses\n\n"
                "Risks:\n"
                "- Over-diversification can limit the potential for outsized, high returns\n\n"
                "Takeaway:\n"
                "Never put all your eggs in one basket. Allocate across cash, bonds, and equities."
            )

        # Default standard education output
        return "Personal Finance", (
            "Topic:\n"
            "Personal Finance\n\n"
            "Explanation:\n"
            "Personal finance is the management of your money through budgeting, saving, investing, and retirement planning.\n\n"
            "Example:\n"
            "Implementing a 50/30/20 rule monthly: 50% on needs, 30% on wants, and 20% directly into savings.\n\n"
            "Benefits:\n"
            "- Builds personal financial independence\n"
            "- Promotes financial preparedness for emergencies\n\n"
            "Risks:\n"
            "- Requires continuous discipline and financial education\n\n"
            "Takeaway:\n"
            "Establishing strong basic budgeting habits is the foundation of all future investing."
        )

    async def get_response(self, request: ChatRequest) -> ChatResponse:
        """
        Coordinates the conversation, validates incoming safety, pulls response,
        runs outgoing safety validation, handles memory states, and returns result.
        """
        message = request.message.strip()
        session_id = request.session_id or "default_session"

        # Init memory if missing
        if session_id not in CONVERSATION_MEMORY:
            CONVERSATION_MEMORY[session_id] = []

        # 1. Inbound safety check
        if self.validate_safety(message):
            logger.warning(f"Prohibited financial request caught in inbound message: '{message}'")
            return ChatResponse(
                topic="General Security",
                response="This assistant provides educational information only and not financial advice."
            )

        history = CONVERSATION_MEMORY[session_id]

        if self.use_mock:
            # 2a. Call Fallback/Mock Education Engine
            topic, response_text = self._get_mock_response(message, history)
        else:
            # 2b. Call live Gemini LLM
            try:
                # Load prompt template
                prompt_dir = os.path.dirname(__file__)
                prompt_path = os.path.join(prompt_dir, "..", "prompts", "investment_system_prompt.txt")
                with open(prompt_path, "r", encoding="utf-8") as f:
                    system_prompt = f.read()

                # Build context prompt containing historical interactions
                full_prompt = system_prompt + "\n\n### Conversation History:\n"
                for user_q, model_a in history:
                    full_prompt += f"User: {user_q}\nAssistant:\n{model_a}\n\n"
                
                full_prompt += f"User: {message}\nAssistant:\n"

                # Send request to Gemini Model
                response = self.model.generate_content(
                    full_prompt,
                    generation_config={"temperature": 0.1, "max_output_tokens": 1200}
                )
                response_text = response.text

                # Parse topic from output
                topic = "Personal Finance"
                if "Topic:" in response_text:
                    parts = response_text.split("Topic:")
                    if len(parts) > 1:
                        topic_line = parts[1].strip().split("\n")[0]
                        topic = topic_line.strip()
            except Exception as e:
                logger.error(f"Gemini API failure during invocation: {e}. Falling back to mock engine.")
                topic, response_text = self._get_mock_response(message, history)

        # 3. Outbound safety check
        if self.validate_safety(response_text):
            logger.warning("Unsafe content detected in generated response. Blocking response.")
            return ChatResponse(
                topic="General Security",
                response="This assistant provides educational information only and not financial advice."
            )

        # 4. Save to history (keep max 5 pairs)
        history.append((message, response_text))
        if len(history) > 5:
            history.pop(0)
        CONVERSATION_MEMORY[session_id] = history

        return ChatResponse(
            topic=topic,
            response=response_text
        )
