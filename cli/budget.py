"""Stuff concerning operating with budgets."""

import json
import os

BUDGET_FILE = "../budget.json"


def load_budget():
    """Load budget data from a JSON file and return it as a dict."""
    if not os.path.exists(BUDGET_FILE) or os.stat(BUDGET_FILE).st_size == 0:
        return {}  # return empty dict for testing
    try:
        with open(BUDGET_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_budget(budget):
    """Save the budget data to a JSON file."""
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        json.dump(budget, f, indent=4)


def set_budget(year, month, amount):
    """Set the budget for a specific month and year."""
    budget = load_budget()
    key = f"{year}-{month:02d}"
    budget[key] = amount
    save_budget(budget)
    print(f"Budget for {key} set to {amount:.2f} PLN")


def get_budget(year, month):
    """Get budget for a specific year and month."""
    budget = load_budget()
    key = f"{year}-{month:02d}"
    if key not in budget:
        raise ValueError("Budget not found for the given month and year.")
    return budget[key]


def delete_budget(year, month):
    """Delete the budget for a specific year and month."""
    budget = load_budget()
    key = f"{year}-{month:02d}"
    if key in budget:
        del budget[key]
        save_budget(budget)
        print(f"Deleted budget for {key}.")
    else:
        print(f"No budget found for {key}.")


def calculate_remaining(year, month, expenses):
    """Calculate remaining budget for a given year and month after expenses."""
    budget = get_budget(year, month)
    total_spent = sum(
        e["price"] for e in expenses if e["date"].startswith(f"{year}-{month:02d}")
    )
    return budget - total_spent


def show_budget(month, year, data):
    """Show the budget for a month and year, or whole year if month=None."""
    budget = load_budget()

    if month is None:
        # For whole year (month not specified)
        print(f"Budget summary for year {year}:")
        total_budget = 0.0
        total_expenses = 0.0

        for m in range(1, 13):
            key = f"{year}-{m:02d}"
            budget_amount = budget.get(key, None)
            if budget_amount is None:
                print(f"  {key}: No budget set.")
                continue

            expenses_sum = sum(e["price"] for e in data if e["date"].startswith(key))
            remaining = budget_amount - expenses_sum

            print(
                f"  {key}: Budget {budget_amount:.2f} PLN, "
                f"Expenses {expenses_sum:.2f} PLN, Remaining {remaining:.2f} PLN"
            )

            total_budget += budget_amount
            total_expenses += expenses_sum

        print("-" * 40)
        print(f"Total budget: {total_budget:.2f} PLN")
        print(f"Total expenses: {total_expenses:.2f} PLN")
        print(f"Total remaining: {total_budget - total_expenses:.2f} PLN")
    else:
        # For specific month
        key = f"{year}-{month:02d}"
        budget_amount = budget.get(key, None)
        if budget_amount is None:
            print(f"No budget set for {key}.")
            return

        expenses_sum = sum(e["price"] for e in data if e["date"].startswith(key))

        print(f"Budget for {key}: {budget_amount:.2f} PLN")
        print(f"Expenses: {expenses_sum:.2f} PLN")
        print(f"Remaining: {budget_amount - expenses_sum:.2f}")
