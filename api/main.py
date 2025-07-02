"""
Backend with FastAPI, mostly trying new things.

It can be really bad, idk.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, conint, confloat
from typing import List, Optional
import datetime

app = FastAPI()


class BudgetItem(BaseModel):
    """Validate Budget item for a specific year and month with a non-negative amount."""

    year: conint(ge=2000, le=2100) = Field(..., description="Budget year, ie. 2025")
    month: conint(ge=1, le=12) = Field(..., description="Budget month, 1-12")
    amount: confloat(ge=0) = Field(..., description="Budget, >= 0")


class ExpenseItem(BaseModel):
    """Validate Expense item."""

    price: confloat(gt=0)
    category: str
    date: datetime.date = Field(default_factory=datetime.date.today)


budgets = {}
expenses: List[ExpenseItem] = []


@app.post("/budget/")
def set_budget(item: BudgetItem):
    """Set the budget, it's not setting budget...yet."""
    key = f"{item.year}-{item.month:02d}"
    budgets[key] = item.amount
    return {"message": f"Budget for {key} set to {item.amount:.2f} PLN"}


@app.get("/budget/{year}/{month}")
def get_budget(year: int, month: int):
    """Get the budget for specific year and/or month."""
    key = f"{year}-{month:02d}"
    amount = budgets.get(key)
    if amount is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return {"year": year, "month": month, "amount": amount}


@app.delete("/budget/{year}/{month}")
def delete_budget(year: int, month: int):
    """Delete the budget for specific year and/or month."""
    key = f"{year}-{month:02d}"
    if key not in budgets:
        raise HTTPException(status_code=404, detail="Budget not found")
    del budgets[key]
    return {"message": f"Budget for {key} deleted"}


@app.post("/expenses/")
def add_expense(expense: ExpenseItem):
    """Add an expense to the budget."""
    expenses.append(expense)
    return {
        "message": f"Added expense: {expense.price:.2f} PLN,"
        f" Category: {expense.category}, Date: {expense.date}"
    }


@app.get("/expenses/", response_model=List[ExpenseItem])
def list_expenses(year: Optional[int] = None, month: Optional[int] = None):
    """List all expenses for a specific year and/or month."""
    filtered = expenses
    if year is not None and month is not None:
        filtered = [
            e for e in expenses if e.date.year == year and e.date.month == month
        ]
    return filtered


@app.delete("/expenses/")
def clear_expenses():
    """Clear all expenses."""
    expenses.clear()
    return {"message": "All expenses deleted"}
