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
BUDGET_FILE = "budget.json"


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


def load_budget():
    """Load budget data from a JSON file and return it as a list."""
    try:
        with open("budget.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_budget(budget):
    """Save the budget data to a JSON file."""
    with open("budget.json", "w") as f:
        json.dump(budget, f, indent=4)


def set_budget(month, year, amount):
    """Set the budget for a specific month and year."""
    if amount <= 0:
        print("Budget amount must be greater than or equal zero.")
        return
    budget = load_budget()
    key = f"{year}-{month:02d}"
    budget[key] = amount
    save_budget(budget)
    print(f"Budget for {key} set to {amount:.2f} PLN")


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
        print(f"Remaining: {budget_amount - expenses_sum:.2f} PLN")


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
            if datetime.datetime.strptime(expense["date"], "%Y-%m-%d").date()
            <= date_from
        ]
    return data


def main():
    """Parse arguments and execute commands."""
    parser = argparse.ArgumentParser()
    # actions
    parser.add_argument("-a", "--add", action="store_true", help="Add an expense.")
    parser.add_argument(
        "--delete",
        type=int,
        help="Delete expense by its index in the list (starting from 1).",
    )
    parser.add_argument(
        "--edit", type=int, help="Edit an expense by its index (1-based)."
    )
    parser.add_argument("-l", "--list", action="store_true", help="List expenses.")
    parser.add_argument("-s", "--sum", action="store_true", help="Sum the expenses.")
    parser.add_argument(
        "--group-by-category", action="store_true", help="Group expenses by category."
    )
    parser.add_argument("--export", help="Export expenses to CSV file.")
    parser.add_argument(
        "--plot", action="store_true", help="Plot expenses by category."
    )

    # filters
    parser.add_argument("--filter-category", help="Show only this category.")
    parser.add_argument(
        "--date-from", help="Show expenses from this date (YYYY-MM-DD)."
    )
    parser.add_argument("--date-to", help="Show expenses up to this date (YYYY-MM-DD).")

    # data
    parser.add_argument("-p", "--price", type=float, help="Amount of the expense.")
    parser.add_argument("-c", "--category", help="Category name for the expense.")
    parser.add_argument("-d", "--date", help="Date of the expense.")

    # budgeting
    parser.add_argument("--set-budget", type=float, help="Set budget amount for month.")
    parser.add_argument("--month", type=int, help="Month for budget (1-12).")
    parser.add_argument("--year", type=int, help="Year for budget (YYYY).")
    parser.add_argument(
        "--show-budget", action="store_true", help="Show budget summary for month/year."
    )

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
        else:
            parsed_date = parse_date(args.date)
            if parsed_date is None:
                return
            args.date = parsed_date.isoformat()

        data = load_data()

        add_expense(data, args.price, args.category, args.date)
        save_data(data)
        print(
            f"Done. Added an expense of {args.price:.2f} PLN"
            f" in category '{args.category}' on {args.date}."
        )
    if args.delete:
        data = load_data()
        deleted_index = args.delete - 1
        if 0 <= deleted_index < len(data):
            removed = data.pop(deleted_index)
            save_data(data)
            print(
                f"Deleted expense: {removed['price']} PLN, "
                f"{removed['category']}, {removed['date']}"
            )
        else:
            print(
                f"Invalid index: {args.delete}. Use --list to see all current expenses."
            )
            return

    if args.edit:
        data = load_data()
        edit_index = args.edit - 1
        if 0 <= edit_index < len(data):
            expense = data[edit_index]
            if args.price:
                expense["price"] = args.price
            if args.category:
                expense["category"] = args.category
            if args.date:
                parsed_date = parse_date(args.date)
                if parsed_date:
                    expense["date"] = parsed_date.isoformat()
            save_data(data)
            print(
                f"Updated expense at position {args.edit}: "
                f"{expense['price']} PLN, {expense['category']}, {expense['date']}"
            )
        else:
            print(
                f"Invalid index: {args.edit}. Use --list to see all current expenses."
            )

    if args.list:
        data = load_data()
        date_from = parse_date(args.date_from) if args.date_from else None
        date_to = parse_date(args.date_to) if args.date_to else None

        data = filter_expenses(data, args.filter_category, date_from, date_to)

        print(f"{'Price':<8} | {'Category':<12} | {'Date'}")
        print("-" * 35)
        for expense in data:
            print(
                f"{expense['price']:<8} | {expense['category']:<12} | {expense['date']}"
            )
        if args.group_by_category:
            if not data:
                print("No expenses to summarize.")
                return
            from collections import defaultdict

            summary = defaultdict(float)
            for expense in data:
                summary[expense["category"]] += float(expense["price"])
            print("\nSum of expenses by category:")
            print(f"{'Category':<12} | {'Total'}")
            print("-" * 25)
            for category, total in summary.items():
                print(f"{category:<12}: {total:.2f} PLN")
            print("-" * 25)

        if args.sum:
            total = sum(expense["price"] for expense in data)

            print(f"{'Total':<8}: {total:.2f} PLN")

    if args.export:
        filename = args.export
        data = load_data()
        with open(filename, "w") as file:
            file.write("Price,Category,Date\n")
            for expense in data:
                file.write(
                    f"{expense['price']},{expense['category']},{expense['date']}\n"
                )
        print(f"Exported {len(data)} expenses to {filename}")

    if args.plot:
        import matplotlib.pyplot as plt
        from collections import defaultdict

        data = load_data()
        summary = defaultdict(float)
        for expense in data:
            summary[expense["category"]] += expense["price"]

        categories = list(summary.keys())
        totals = list(summary.values())

        plt.figure(figsize=(8, 5))
        plt.bar(categories, totals, color="cyan")
        plt.xlabel("Category")
        plt.ylabel("Total Expenses")
        plt.title("Expenses by Category")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    if args.set_budget is not None:
        if args.month is None or args.year is None:
            print("Please specify --month and --year when setting budget.")
            return
        set_budget(args.month, args.year, args.set_budget)
        return

    if args.show_budget:
        if args.month is None or args.year is None:
            today = datetime.date.today()
            month = today.month
            year = today.year
        else:
            month = args.month
            year = args.year
        data = load_data()
        show_budget(month, year, data)
        return


if __name__ == "__main__":
    main()
