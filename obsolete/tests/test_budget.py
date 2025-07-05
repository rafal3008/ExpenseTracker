"""Testfile for budget.py, because of The great main schism."""

import tempfile
import json
import os
import pytest
from obsolete.cli import budget


def test_set_and_show_budget():
    """Sets budget and verify retrieval."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        budget.BUDGET_FILE = f.name
    try:
        budget.set_budget(2025, 7, 500)
        amount = budget.get_budget(2025, 7)
        assert amount == 500
    finally:
        os.remove(budget.BUDGET_FILE)


def test_no_budget_set():
    """Try for error if budget not set before calculation."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        budget.BUDGET_FILE = f.name

    expenses = [
        {"price": 50, "category": "food", "date": "2025-07-01"},
    ]

    try:
        with pytest.raises(ValueError) as excinfo:
            budget.calculate_remaining(2025, 7, expenses)
        assert "Budget not found" in str(excinfo.value)
    finally:
        os.remove(budget.BUDGET_FILE)


def test_delete_budget():
    """Set and delete budget; verify deletion."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        budget.BUDGET_FILE = f.name

    try:
        budget.set_budget(2025, 7, 500)
        budget.delete_budget(2025, 7)
        with pytest.raises(ValueError):
            budget.get_budget(2025, 7)
    finally:
        os.remove(budget.BUDGET_FILE)


def test_calculate_remaining():
    """Calculate remaining budget after expenses."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        budget.BUDGET_FILE = f.name

    expenses = [
        {"price": 50, "category": "food", "date": "2025-07-01"},
        {"price": 30, "category": "transport", "date": "2025-07-15"},
        {"price": 20, "category": "food", "date": "2025-08-01"},
    ]

    try:
        budget.set_budget(2025, 7, 500)
        remaining = budget.calculate_remaining(2025, 7, expenses)
        assert remaining == 420  # 500 - (50+30)
    finally:
        os.remove(budget.BUDGET_FILE)


def test_show_budget_for_whole_year_and_month(capfd):
    """Prepare monthly budget, add few expences, test what if empty."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        budget.BUDGET_FILE = f.name

    budgets = {
        "2025-07": 500.0,
        "2025-08": 300.0,
    }
    with open(budget.BUDGET_FILE, "w", encoding="utf-8") as f:
        json.dump(budgets, f, indent=4)

    expenses = [
        {"price": 50, "category": "food", "date": "2025-07-01"},
        {"price": 100, "category": "transport", "date": "2025-07-15"},
        {"price": 80, "category": "food", "date": "2025-08-01"},
    ]

    budget.show_budget(None, 2025, expenses)
    out, err = capfd.readouterr()
    assert "Budget summary for year 2025" in out
    assert "2025-07: Budget 500.00 PLN" in out
    assert "2025-08: Budget 300.00 PLN" in out
    assert "Expenses 150.00 PLN" in out
    assert "Expenses 80.00 PLN" in out
    assert "Total budget: 800.00 PLN" in out
    assert "Total expenses: 230.00 PLN" in out
    assert "Total remaining: 570.00 PLN" in out

    budget.show_budget(7, 2025, expenses)
    out, err = capfd.readouterr()
    assert "Budget for 2025-07: 500.00 PLN" in out
    assert "Expenses: 150.00 PLN" in out
    assert "Remaining: 350.00" in out

    budget.show_budget(9, 2025, expenses)
    out, err = capfd.readouterr()
    assert "No budget set for 2025-09." in out

    os.remove(budget.BUDGET_FILE)
