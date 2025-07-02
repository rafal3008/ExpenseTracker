"""
Backend with FastAPI, mostly trying new things.

It can be really bad, idk.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, conint, confloat  # Validating data
from typing import Optional
import datetime
from cli import expenses

app = FastAPI()

budgets = []


class BudgetItem(BaseModel):
    """Validate Budget item for a specific year and month with a non-negative amount."""

    year: conint(ge=2000, le=2100) = Field(..., description="Budget year, ie. 2025")
    month: conint(ge=1, le=12) = Field(..., description="Budget month, 1-12")
    amount: confloat(ge=0) = Field(..., description="Budget, >= 0")


class ExpenseItem(BaseModel):
    """Validate Expense item."""

    price: confloat(gt=0)
    category: str
    date: Optional[datetime.date] = Field(default_factory=datetime.date.today)


@app.post("/budget/")
def set_budget(item: BudgetItem):
    """Set the budget, it's not setting budget...yet."""
    key = f"{item.year}-{item.month:02d}"
    budgets[key] = item.amount
    return {"message": f"Budget for {key} set to {item.amount:.2f} PLN"}


@app.get("/budget/{year}/{month}")
def get_budget(year: int, month: int):
    """Get the budget. Same like last one - it should do sth, but it's not."""
    key = f"{year}-{month:02d}"
    amount = budgets.get(key)
    if amount is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return {"year": year, "month": month, "amount": amount}


@app.post("/expenses/")
def add_expense(expense: ExpenseItem):
    """Add an expense to the budget."""
    expenses.append(expense.dict())
    return {
        "message": f"Added expense: {expense.price:.2f} "
        f"PLN, Category: {expense.category}, Date: {expense.date}"
    }
