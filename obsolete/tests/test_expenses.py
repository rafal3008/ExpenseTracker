"""Testfile for expenses.py, because of The great main schism."""

import datetime
import tempfile
import json
import os

from obsolete.cli import expenses


def test_add_and_load_expense():
    """Test adding and loading an expense from a JSON file."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        filename = f.name
    try:
        # empty JSON file, because it needs initializing
        # before doing anything
        with open(filename, "w") as f2:
            json.dump([], f2)

        expenses.DATA_FILE = filename

        data = expenses.load_data()
        assert data == []

        expenses.add_expense(data, 50.0, "food", "2025-07-02")

        # proper testing starts here
        data = expenses.load_data()
        assert len(data) == 1
        assert data[0]["price"] == 50.0
        assert data[0]["category"] == "food"
        assert data[0]["date"] == "2025-07-02"
    finally:
        os.remove(filename)


def test_filter_by_category():
    """Test filtering expenses by category."""
    data = [
        {"price": 10, "category": "food", "date": "2025-07-01"},
        {"price": 20, "category": "transport", "date": "2025-07-02"},
    ]
    result = expenses.filter_expenses(data, category="food")
    assert len(result) == 1
    assert result[0]["category"] == "food"


def test_filter_by_date_range():
    """Test filtering expenses by a date range."""
    data = [
        {"price": 10, "category": "food", "date": "2025-07-01"},
        {"price": 20, "category": "transport", "date": "2025-07-10"},
        {"price": 30, "category": "food", "date": "2025-07-20"},
    ]
    date_from = datetime.date(2025, 7, 5)
    date_to = datetime.date(2025, 7, 15)
    result = expenses.filter_expenses(data, date_from=date_from, date_to=date_to)
    assert len(result) == 1
    assert result[0]["date"] == "2025-07-10"


def test_edit_expense():
    """Test editing an existing expense."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        filename = f.name
    try:
        expenses.DATA_FILE = filename
        data = []
        expenses.add_expense(data, 10, "food", "2025-07-01")
        expenses.edit_expense(data, 0, price=25, category="coffee", date="2025-07-05")
        data = expenses.load_data()
        assert data[0]["price"] == 25
        assert data[0]["category"] == "coffee"
        assert data[0]["date"] == "2025-07-05"
    finally:
        os.remove(filename)


def test_delete_expense():
    """Test removing expenses."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        filename = f.name
    try:
        expenses.DATA_FILE = filename
        data = []
        expenses.add_expense(data, 10, "food", "2025-07-01")
        expenses.delete_expense(data, 0)
        data = expenses.load_data()
        assert data == []
    finally:
        os.remove(filename)
