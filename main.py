"""
A project that’s never finished, approach n.

Expense management module:
-loads data from a JSON file,
-saves new expenses,
-analyzes budget overruns.
"""

import json
import os
import datetime

DATA_FILE = "data.json"


def load_data():
    """Load expenses data from a JSON file and return it as a list."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as json_file:
        data = json.load(json_file)
        return data


def save_data(data):
    """Save the expenses data list to a JSON file."""
    with open(DATA_FILE, "w") as json_file:
        json.dump(data, json_file, indent=4)


def add_expense(data, price, category, date=None):
    """
    Add an expense to the list of expenses.

    Args:
        data (list): List of current expenses.
        price (float): Amount of the expense.
        category (str): Category name for the expense.
        date (str, optional): Date of the expense in YYYY-MM-DD format.
                              Defaults to today's date if None.
    """
    if date is None:
        date = datetime.date.today().isoformat()
    expense = {"price": price, "category": category, "date": date}
    data.append(expense)
