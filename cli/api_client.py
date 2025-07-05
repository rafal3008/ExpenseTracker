"""This should communicate with api...should."""

import requests

API_URL = "http://127.0.0.1:8000"


def set_budget(year, month, amount):
    """Set budget."""
    data = {"year": year, "month": month, "amount": amount}
    r = requests.post(f"{API_URL}/budget/", json=data)
    r.raise_for_status()
    return r.json()


def get_budget(year, month):
    """Get the budget for a specific year and month."""
    r = requests.get(f"{API_URL}/budget/{year}/{month}/")
    r.raise_for_status()
    return r.json()


def delete_budget(year, month):
    """Delete budget."""
    r = requests.delete(f"{API_URL}/budget/{year}/{month}/")
    r.raise_for_status()
    return r.json()


def add_expense(price, category, date=None):
    """Add an expense."""
    data = {"price": price, "category": category}
    if date:
        data["date"] = date
    r = requests.post(f"{API_URL}/expenses/", json=data)
    r.raise_for_status()
    return r.json()


def list_expenses(year=None, month=None):
    """List all expenses for a given year/month."""
    params = {}
    if year:
        params["year"] = year
    if month:
        params["month"] = month
    r = requests.get(f"{API_URL}/expenses/", params=params)
    r.raise_for_status()
    return r.json()


def edit_expense(index, price=None, category=None, date=None):
    """Edit an expense."""
    data = {}
    if price is not None:
        data["price"] = price
    if category is not None:
        data["category"] = category
    if date is not None:
        data["date"] = date
    r = requests.put(f"{API_URL}/expenses/{index}", json=data)
    r.raise_for_status()
    return r.json()


def clear_expenses():
    """Clear all expenses."""
    r = requests.delete(f"{API_URL}/expenses")
    r.raise_for_status()
    return r.json()
