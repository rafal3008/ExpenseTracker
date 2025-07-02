"""Testfile for budget.py, because of The great main schism."""

import tempfile
import os
import json

from cli import budget


def test_set_and_show_budget():
    """Sets budget and calculate remaining budget after adding few expenses."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        filename = f.name
    try:
        budget.BUDGET_FILE = filename
        data = [
            {"price": 50, "category": "food", "date": "2025-07-01"},
            {"price": 30, "category": "transport", "date": "2025-07-15"},
            {"price": 20, "category": "food", "date": "2025-08-01"},
        ]

        # set budget
        budget.set_budget(7, 2025, 500)

        # verify file
        with open(filename, "r") as f_json:
            saved = json.load(f_json)
        assert saved["2025-07"] == 500

        # show budget
        remaining = budget.calculate_remaining(7, 2025, data)
        assert remaining["budget"] == 500
        assert remaining["expenses_sum"] == 80
        assert remaining["remaining"] == 420
    finally:
        os.remove(filename)


def test_no_budget_set():
    """Sets budget when there is no budget set yet."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        filename = f.name
    try:
        budget.BUDGET_FILE = filename
        data = [
            {"price": 50, "category": "food", "date": "2025-07-01"},
        ]
        # without the budget
        result = budget.calculate_remaining(7, 2025, data)
        assert result["budget"] is None
        assert result["expenses_sum"] == 50
    finally:
        os.remove(filename)
