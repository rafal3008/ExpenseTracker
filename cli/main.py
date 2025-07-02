"""
A project that’s never finished, approach n.

Expense management module:
-loads data from a JSON file,
-saves new expenses,
-analyzes budget overruns.
"""

import argparse
import datetime
from expenses import (
    load_data,
    add_expense,
    filter_expenses,
    edit_expense,
    delete_expense,
)
from budget import set_budget, show_budget
from plotting import plot_expenses_by_category


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
    parser.add_argument(
        "--year", type=int, required=True, help="Year for budget (YYYY)."
    )
    parser.add_argument(
        "--month", type=int, choices=range(1, 12), help="Month for budget (1-12)."
    )
    parser.add_argument(
        "--set-budget", type=float, help="Set budget amount for month/year."
    )
    parser.add_argument(
        "--show-budget", action="store_true", help="Show budget summary for month/year."
    )

    args = parser.parse_args()
    data = load_data()

    if args.set_budget is not None:
        if args.month is None or args.year is None:
            print("Please specify --month and --year when setting budget.")
            return
        set_budget(args.month, args.year, args.set_budget)
        return

    if args.show_budget:
        today = datetime.date.today()
        month = args.month  # może być None
        year = args.year if args.year else today.year
        data = load_data()
        show_budget(month, year, data)
        return

    if args.add:
        price = float(args.add[0])
        category = args.add[1]
        add_expense(data, price, category, args.date)
        return

    if args.filter:
        date_from = (
            datetime.date.fromisoformat(args.date_from) if args.date_from else None
        )
        date_to = datetime.date.fromisoformat(args.date_to) if args.date_to else None
        filtered = filter_expenses(
            data, category=args.category, date_from=date_from, date_to=date_to
        )
        for i, e in enumerate(filtered):
            print(f"{i}: {e['price']:.2f} PLN, {e['category']}, {e['date']}")
        return

    if args.edit:
        index = int(args.edit[0])
        price = float(args.edit[1]) if len(args.edit) > 1 else None
        category = args.edit[2] if len(args.edit) > 2 else None
        date = args.edit[3] if len(args.edit) > 3 else None
        edit_expense(data, index, price, category, date)
        return

    if args.delete is not None:
        delete_expense(data, args.delete)
        return

    if args.plot:
        plot_expenses_by_category(data)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
