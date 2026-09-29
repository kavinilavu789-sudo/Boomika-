import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
).strip()


def fallback_recommendation(
    budget: float,
    category: str,
    description: str = ""
):
    """
    Local fallback recommendation.
    Used when Gemini is unavailable.
    """

    try:
        budget = float(budget)
    except (TypeError, ValueError):
        budget = 0.0

    category_lower = str(category).lower().strip()

    # --------------------------------------------------------
    # PARTY
    # --------------------------------------------------------

    if category_lower == "party":

        food = budget * 0.45
        venue = budget * 0.25
        decoration = budget * 0.10
        entertainment = budget * 0.10
        emergency = budget * 0.10

        recommendation = f"""
Party Budget Plan

Total Budget: ₹{budget:,.0f}

Suggested Allocation:

• Food & Catering: ₹{food:,.0f}
• Venue & Essentials: ₹{venue:,.0f}
• Decoration: ₹{decoration:,.0f}
• Entertainment: ₹{entertainment:,.0f}
• Emergency/Extra: ₹{emergency:,.0f}

Money-saving tips:

• Compare food and decoration prices before booking.
• Keep some money aside for unexpected expenses.
"""

    # --------------------------------------------------------
    # JEWELRY
    # --------------------------------------------------------

    elif category_lower == "jewelry":

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

    # --------------------------------------------------------
    # HOME / DEFAULT
    # --------------------------------------------------------

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
    """
    Generate budget recommendation using Gemini.

    If Gemini is unavailable, the local fallback
    recommendation is returned automatically.
    """

    # --------------------------------------------------------
    # VALIDATE BUDGET
    # --------------------------------------------------------

    try:
        budget = float(budget)
    except (TypeError, ValueError):

        return {
            "success": False,
            "source": "validation",
            "recommendation": "Please enter a valid budget amount."
        }

    if budget <= 0:

        return {
            "success": False,
            "source": "validation",
            "recommendation": "Please enter a budget greater than ₹0."
        }

    # --------------------------------------------------------
    # CLEAN INPUT
    # --------------------------------------------------------

    category = str(category or "Home").strip()
    description = str(description or "").strip()

    # --------------------------------------------------------
    # API KEY CHECK
    # --------------------------------------------------------

    if not GEMINI_API_KEY:

        print()
        print("=" * 60)
        print("GEMINI API KEY NOT FOUND")
        print("=" * 60)
        print("Using local fallback recommendation.")
        print()

        return fallback_recommendation(
            budget,
            category,
            description
        )

    # --------------------------------------------------------
    # PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are PocketSmart AI, a smart personal budget planning assistant.

User budget: ₹{budget:,.0f}
Category: {category}
Description: {description}

Create a simple and practical budget recommendation.

Include:

1. Suggested expense categories
2. Suggested amount for each category
3. Savings suggestion
4. One or two useful money-saving tips

Requirements:

- Keep the answer concise.
- Make the recommendation practical.
- Use Indian Rupees (₹).
- Do not use complicated financial terminology.
- Do not ask follow-up questions.
- Do not include unnecessary explanations.
- Make sure the suggested amounts are reasonable for the total budget.
"""

    # --------------------------------------------------------
    # GEMINI REQUEST
    # --------------------------------------------------------

    try:

        print()
        print("Calling Gemini API...")
        print("Gemini model:", GEMINI_MODEL)
        print("Thinking level: low")

        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=500,
                thinking_config=types.ThinkingConfig(
                    thinking_level="low"
                )
            )
        )

        # ----------------------------------------------------
        # EMPTY RESPONSE
        # ----------------------------------------------------

        if response is None:

            print()
            print("Gemini returned an empty response.")
            print("Using local fallback recommendation.")
            print()

            return fallback_recommendation(
                budget,
                category,
                description
            )

        # ----------------------------------------------------
        # GET TEXT
        # ----------------------------------------------------

        recommendation_text = getattr(
            response,
            "text",
            None
        )

        if not recommendation_text:

            print()
            print("Gemini returned no text.")
            print("Using local fallback recommendation.")
            print()

            return fallback_recommendation(
                budget,
                category,
                description
            )

        recommendation_text = recommendation_text.strip()

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        print()
        print("=" * 60)
        print("GEMINI API CALL SUCCESSFUL")
        print("=" * 60)
        print()

        return {
            "success": True,
            "source": "gemini",
            "recommendation": recommendation_text
        }

    # --------------------------------------------------------
    # ERROR HANDLING
    # --------------------------------------------------------

    except Exception as e:

        print()
        print("=" * 60)
        print("GEMINI API ERROR")
        print("=" * 60)

        print("Error type:", type(e).__name__)
        print("Error:", str(e))

        print("=" * 60)
        print("Using local fallback recommendation.")
        print()

        return fallback_recommendation(
            budget,
            category,
            description
        )