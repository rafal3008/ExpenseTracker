"""
Backend with FastAPI, mostly trying new things.

It can be really bad, idk.
"""

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field, conint, confloat
from typing import List, Optional
import datetime

from api.storage import load_expenses, save_expenses, load_budget, save_budget

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


@app.post("/budget/")
def set_budget(item: BudgetItem):
    """Set the budget, it's not setting budget...yet."""
    key = f"{item.year}-{item.month:02d}"
    budget_data = load_budget()
    budget_data[key] = item.amount
    save_budget(budget_data)
    return {"message": f"Budget for {key} set to {item.amount:.2f} PLN"}


@app.get("/budget/{year}/{month}")
def get_budget(year: int, month: int):
    """Get the budget for specific year and/or month."""
    key = f"{year}-{month:02d}"
    budget_data = load_budget()
    amount = budget_data.get(key)
    if amount is None:
        raise HTTPException(status_code=404, detail="Budget not found")

    expenses_data = load_expenses()
    spent = sum(
        expense["price"] for expense in expenses_data if expense["date"].startswith(key)
    )
    remaining_amount = amount - spent

    warning = None
    if amount > 0 and spent / amount >= 0.8:  # over 80% of budget spent
        warning = f"You've spent {spent / amount: .0%} of your budget!"

    return {
        "year": year,
        "month": month,
        "budget": amount,
        "spent": spent,
        "remaining": remaining_amount,
        "warning": warning,
    }


@app.delete("/budget/{year}/{month}")
def delete_budget(year: int, month: int):
    """Delete the budget for specific year and/or month."""
    key = f"{year}-{month:02d}"
    budget_data = load_budget()
    if key not in budget_data:
        raise HTTPException(status_code=404, detail="Budget not found")
    del budget_data[key]
    save_budget(budget_data)
    return {"message": f"Budget for {key} deleted"}


@app.post("/expenses/")
def add_expense(expense: ExpenseItem):
    """Add an expense to the budget."""
    expenses_data = load_expenses()
    new_expense = {
        "price": expense.price,
        "category": expense.category,
        "date": expense.date.isoformat(),
    }
    expenses_data.append(new_expense)
    save_expenses(expenses_data)
    return {
        "message": f"Added expense: {expense.price:.2f} PLN,"
        f" Category: {expense.category}, Date: {expense.date}"
    }


@app.delete("/expenses/{index}")
def delete_expense(index: int = Path(..., ge=0)):
    """Delete an expense by index."""
    expenses_data = load_expenses()
    if index >= len(expenses_data):
        raise HTTPException(status_code=404, detail="Expense not found")
    deleted_expense = expenses_data.pop(index)
    save_expenses(expenses_data)
    return {
        "message": f"Deleted expense: {deleted_expense['price']} "
        f"PLN, Category: {deleted_expense['category']}, "
        f"Date: {deleted_expense['date']}"
    }


@app.get("/expenses/", response_model=List[ExpenseItem])
def list_expenses(year: Optional[int] = None, month: Optional[int] = None):
    """List all expenses for a specific year and/or month."""
    expenses_data = load_expenses()

    if year is not None and month is not None:
        key = f"{year}-{month:02d}"
        filtered = [
            expense for expense in expenses_data if expense["date"].startswith(key)
        ]
    else:
        filtered = expenses_data

    return [
        ExpenseItem(
            price=expense["price"],
            category=expense["category"],
            date=datetime.date.fromisoformat(expense["date"]),
        )
        for expense in filtered
    ]


@app.delete("/expenses/")
def clear_expenses():
    """Clear all expenses_data."""
    save_expenses(None)
    return {"message": "All expenses deleted"}


@app.patch("/expenses/{index}")
def edit_expense(
    index: int = Path(
        ..., ge=0
    ),  # Reguired in url, validation - grater or equal than 0
    price: Optional[confloat(gt=0)] = None,
    category: Optional[str] = None,
    date: Optional[datetime.date] = None,
):
    """Edit an expense."""
    expenses_data = load_expenses()
    if index >= len(expenses_data):
        raise HTTPException(status_code=404, detail="Expense not found")

    if price is not None:
        expenses_data[index]["price"] = price
    if category is not None:
        expenses_data[index]["category"] = category
    if date is not None:
        expenses_data[index]["date"] = date.isoformat()

    save_expenses(expenses_data)
    return {"message": f"Expense at index {index} updated."}
