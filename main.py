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


def parse_date(date_str):
    """Parse a date string into a datetime."""
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print(f"Invalid date format: {date_str}. Use YYYY-MM-DD.")
        return None


def main():
    """Parse arguments and execute commands."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--add", action="store_true", help="Add an expense.")
    parser.add_argument("-l", "--list", action="store_true", help="List expenses.")
    parser.add_argument("--filter-category", help="Show only this category.")
    parser.add_argument(
        "--date-from", help="Show expenses from this date (YYYY-MM-DD)."
    )
    parser.add_argument("--date-to", help="Show expenses up to this date (YYYY-MM-DD).")
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
            f"Done. Added an expense of {args.price:.2f} PLN"
            f" in category '{args.category}' on {args.date}."
        )

    if args.list:
        data = load_data()

        if args.filter_category:
            data = [
                expense
                for expense in data
                if expense["category"] == args.filter_category
            ]

        if args.date_from:
            date_from = parse_date(args.date_from)
            if date_from is not None:
                data = [
                    expense
                    for expense in data
                    if datetime.datetime.strptime(expense["date"], "%Y-%m-%d").date()
                    >= date_from
                ]

        if args.date_to:
            date_to = parse_date(args.date_to)
            if date_to is not None:
                data = [
                    expense
                    for expense in data
                    if datetime.datetime.strptime(expense["date"], "%Y-%m-%d").date()
                    <= date_to
                ]
        print(f"{'Price':<8} | {'Category':<12} | {'Date'}")
        print("-" * 35)
        for expense in data:
            print(
                f"{expense['price']:<8} | {expense['category']:<12} | {expense['date']}"
            )


if __name__ == "__main__":
    main()
