"""Stuff concerning operating with expenses."""

import json
import datetime
import os


DATA_FILE = "data.json"


def load_data():
    """Load expenses data from a JSON file and return it as a list."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    """Save the expenses data list to a JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_expense(data, price, category, date=None):
    """
    Add an expense to the list of expenses.

    Args:
        data (list): List of current expenses.
        price (float): Amount of the expense.
        category (str): Category name for the expense.
        date (str, optional): Date of the expense in YYYY-MM-DD format.
                              Defaults to None.
    """
    if date is None:
        date = datetime.date.today().isoformat()
    expense = {"price": price, "category": category, "date": date}
    data.append(expense)
    print(f"Added expense: {price:.2f} PLN, Category: {category}, Date: {date}")


def filter_expenses(data, category=None, date_from=None, date_to=None):
    """Filter expenses based on category and date."""
    if category:
        data = [expense for expense in data if expense["category"] == category]
    if date_from:
        data = [
            expense
            for expense in data
            if datetime.datetime.strptime(expense["date"], "%Y-%m-%d").date()
            >= date_from
        ]
    if date_to:
        data = [
            expense
            for expense in data
            if datetime.datetime.strptime(expense["date"], "%Y-%m-%d").date() <= date_to
        ]
    return data


def edit_expense(data, index, price=None, category=None, date=None):
    """Edit expense, based on index."""
    if index < 0 or index >= len(data):
        print("Invalid expense index.")
        return
    if price is not None:
        data[index]["price"] = price
    if category is not None:
        data[index]["category"] = category
    if date is not None:
        data[index]["date"] = date
    save_data(data)
    print(f"Edited expense at index {index}.")


def delete_expense(data, index):
    """Delete expense from data by index."""
    if index < 0 or index >= len(data):
        print("Invalid expense index.")
        return
    removed = data.pop(index)
    save_data(data)
    print(f"Deleted expense: {removed}")
