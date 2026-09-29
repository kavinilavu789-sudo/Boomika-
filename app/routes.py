from fastapi import APIRouter

from .models import (
    HomeBudgetRequest,
    PartyBudgetRequest,
    JewelryBudgetRequest,
)

from ai.gemini_service import generate_budget_recommendation


router = APIRouter(prefix="/api", tags=["Budget"])


@router.post("/home")
def home_budget(data: HomeBudgetRequest):

    ai_result = generate_budget_recommendation(
        budget=data.budget,
        category=data.category,
        description=data.description,
    )

    return {
        "success": True,
        "type": "Home Budget",
        "budget": data.budget,
        "category": data.category,
        "description": data.description,
        "ai_recommendation": ai_result,
    }


@router.post("/party")
def party_budget(data: PartyBudgetRequest):

    description = (
        f"{data.description}. "
        f"Number of guests: {data.guests}"
    )

    ai_result = generate_budget_recommendation(
        budget=data.budget,
        category=data.category,
        description=description,
    )

    return {
        "success": True,
        "type": "Party Budget",
        "budget": data.budget,
        "category": data.category,
        "guests": data.guests,
        "description": data.description,
        "ai_recommendation": ai_result,
    }


@router.post("/jewelry")
def jewelry_budget(data: JewelryBudgetRequest):

    description = (
        f"{data.description}. "
        f"Jewelry item: {data.item_type}"
    )

    ai_result = generate_budget_recommendation(
        budget=data.budget,
        category=data.category,
        description=description,
    )

    return {
        "success": True,
        "type": "Jewelry Budget",
        "budget": data.budget,
        "category": data.category,
        "item_type": data.item_type,
        "description": data.description,
        "ai_recommendation": ai_result,
    }