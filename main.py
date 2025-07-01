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
import argparse

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
                              Defaults to None.
    """
    expense = {"price": price, "category": category, "date": date}
    data.append(expense)


def main():
    """Parse arguments and execute commands."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--add", action="store_true", help="Add an expense.")
    parser.add_argument("-p", "--price", type=float, help="Amount of the expense.")
    parser.add_argument("-c", "--category", help="Category name for the expense.")
    parser.add_argument("-d", "--date", help="Date of the expense.")
    args = parser.parse_args()

    if args.add:

        if args.price is None:
            print("You must specify a price.")
            return
        if args.price <= 0:
            print("Price must be greater than zero.")
            return
        if args.category is None:
            args.category = "Uncategorized"
        if args.date is None:
            args.date = datetime.date.today().isoformat()
        data = load_data()
        add_expense(data, args.price, args.category, args.date)
        save_data(data)
        print(
            f"Done. Added an expense of {args.price} PLN"
            f" in category '{args.category}' on {args.date}."
        )


if __name__ == "__main__":
    main()
