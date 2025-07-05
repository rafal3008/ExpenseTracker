"""Storage methods and json file handling used for fastAPI."""

import json
import os

EXPENSES_FILE = os.getenv("EXPENSES_FILE", "expenses.json")
BUDGET_FILE = os.getenv("BUDGET_FILE", "budget.json")


def load_expenses():
    """Load expenses from json file."""
    if not os.path.exists(EXPENSES_FILE):
        return []
    with open(EXPENSES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_expenses(expenses):
    """Save the expenses to file."""
    with open(EXPENSES_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2)


def load_budget():
    """Load budget from file."""
    if not os.path.exists(BUDGET_FILE):
        return {}
    with open(BUDGET_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_budget(budget):
    """Save budget to file."""
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        json.dump(budget, f, indent=2)
