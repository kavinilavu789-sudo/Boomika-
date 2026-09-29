from pydantic import BaseModel
from typing import Optional


class BudgetRequest(BaseModel):
    budget: float
    category: str
    description: Optional[str] = ""


class HomeBudgetRequest(BudgetRequest):
    pass


class PartyBudgetRequest(BudgetRequest):
    guests: int = 1


class JewelryBudgetRequest(BudgetRequest):
    item_type: str = "General"