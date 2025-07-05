"""
A project that’s never finished, approach n.

Expense management module:
-loads data from a JSON file,
-saves new expenses,
-analyzes budget overruns.
"""

import argparse
import datetime

import api_client

# BUDGET_FILE = os.getenv("BUDGET_FILE", "budget.json")
# DATA_FILE = os.getenv("DATA_FILE", "expenses.json")


def main():
    """Parse arguments and execute commands."""
    parser = argparse.ArgumentParser()
    # actions
    parser.add_argument(
        "--add",
        nargs="+",
        metavar=("PRICE", "CATEGORY", "DATE"),
        help="Add an expense: PRICE [CATEGORY] [DATE]",
    )
    parser.add_argument(
        "--delete",
        type=int,
        help="Delete expense by its index in the list (starting from 1).",
    )
    parser.add_argument(
        "--edit",
        nargs=4,
        metavar=("INDEX", "PRICE", "CATEGORY", "DATE"),
        help="Edit an expense: INDEX PRICE CATEGORY DATE (use 'None' to skip).",
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
    parser.add_argument(
        "--clear-expenses", action="store_true", help="Delete all expenses."
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
    parser.add_argument(
        "--year", type=int, required=True, help="Year for budget (YYYY)."
    )
    parser.add_argument(
        "--month", type=int, choices=range(1, 13), help="Month for budget (1-12)."
    )
    parser.add_argument(
        "--set-budget", type=float, help="Set budget amount for month/year."
    )
    parser.add_argument(
        "--show-budget", action="store_true", help="Show budget summary for month/year."
    )

    args = parser.parse_args()

    if args.show_budget:
        if args.year is None or args.month is None:
            print("Please specify --year and --month to show budget.")
            return
        resp = api_client.get_budget(args.year, args.month)
        print(f"Budget for {args.year}-{args.month:02d}: {resp['budget']:.2f} PLN")
        print(f"Spent: {resp['spent']:.2f} PLN")
        print(f"Remaining: {resp['remaining']:.2f} PLN")
        if resp.get("warning"):
            print("Warning:", resp["warning"])
        return

    if args.set_budget:
        if args.year is None or args.month is None:
            print("Please specify --year and --month when setting budget.")
            return
        resp = api_client.set_budget(args.year, args.month, args.set_budget)
        print(resp["message"])
        return

    if args.add:
        price_str = args.add[0]
        category = "Misc"
        date_str = datetime.date.today().isoformat()

        if len(args.add) >= 2 and args.add[1] and args.add[1].lower() != "none":
            category = args.add[1]
        if len(args.add) >= 3 and args.add[2] and args.add[2].lower() != "none":
            date_str = args.add[2]

        price = float(price_str)

        resp = api_client.add_expense(price, category, date_str)
        print(resp["message"])
        return

    if args.delete is not None:
        index = args.delete - 1  # API expects 0-based
        resp = api_client.delete_expense(index)
        print(resp["message"])
        return

    if args.edit:
        index_str, price_str, category, date = args.edit
        index = int(index_str) - 1
        price = None if price_str.lower() == "none" else float(price_str)
        category = None if category.lower() == "none" else category
        date = None if date.lower() == "none" else date
        resp = api_client.edit_expense(index, price, category, date)
        print(resp["message"])
        return

    if args.list:
        expenses = api_client.get_expenses()
        if not expenses:
            print("No expenses found.")
            return
        for i, exp in enumerate(expenses, start=1):
            print(f"{i}. {exp['price']:.2f} PLN, {exp['category']}, {exp['date']}")
        return

    parser.print_help()

    if args.clear_expenses:
        resp = api_client.clear_expenses()
        print(resp["message"])
        return


if __name__ == "__main__":
    main()
