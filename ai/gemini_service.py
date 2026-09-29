import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


def fallback_recommendation(
    budget: float,
    category: str,
    description: str = ""
):
    """
    Provides a basic recommendation when Gemini is
    temporarily unavailable.
    """

    if category.lower() == "party":
        essentials = budget * 0.45
        food = budget * 0.25
        decoration = budget * 0.10
        entertainment = budget * 0.10
        emergency = budget * 0.10

        recommendation = f"""
Party Budget Plan

Total Budget: ₹{budget:,.0f}

Suggested Allocation:

• Food & Catering: ₹{essentials:,.0f}
• Venue & Essentials: ₹{food:,.0f}
• Decoration: ₹{decoration:,.0f}
• Entertainment: ₹{entertainment:,.0f}
• Emergency/Extra: ₹{emergency:,.0f}

Money-saving tips:
• Compare food and decoration prices before booking.
• Keep some money aside for unexpected expenses.
"""

    elif category.lower() == "jewelry":
        purchase = budget * 0.75
        making = budget * 0.10
        savings = budget * 0.15

        recommendation = f"""
Jewelry Budget Plan

Total Budget: ₹{budget:,.0f}

Suggested Allocation:

• Jewelry Purchase: ₹{purchase:,.0f}
• Making/Additional Charges: ₹{making:,.0f}
• Extra/Savings: ₹{savings:,.0f}

Money-saving tips:
• Compare prices from different stores.
• Ask for a complete price breakdown before purchasing.
"""

    else:
        essentials = budget * 0.50
        savings = budget * 0.20
        personal = budget * 0.20
        emergency = budget * 0.10

        recommendation = f"""
Home Budget Plan

Total Budget: ₹{budget:,.0f}

Suggested Allocation:

• Essential Expenses: ₹{essentials:,.0f}
• Savings: ₹{savings:,.0f}
• Personal Expenses: ₹{personal:,.0f}
• Emergency/Other: ₹{emergency:,.0f}

Money-saving tips:
• Track your daily expenses.
• Avoid unnecessary purchases.
"""

    return {
        "success": True,
        "source": "fallback",
        "recommendation": recommendation.strip()
    }


def generate_budget_recommendation(
    budget: float,
    category: str,
    description: str = ""
):
    prompt = f"""
You are TacketSmart AI, a smart budget planning assistant.

User budget: ₹{budget}
Category: {category}
Description: {description}

Create a simple and practical budget recommendation.

Include:
1. Suggested expense categories
2. Suggested amount for each category
3. Savings suggestion
4. One or two useful money-saving tips

Keep the answer easy to understand.
"""

    if not GEMINI_API_KEY:
        return fallback_recommendation(
            budget,
            category,
            description
        )

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return {
            "success": True,
            "source": "gemini",
            "recommendation": response.text
        }

    except Exception:
        # Gemini temporarily unavailable:
        # use local fallback recommendation.
        return fallback_recommendation(
            budget,
            category,
            description
        )