"""Plotting and statistics."""

import matplotlib.pyplot as plt
from collections import defaultdict


def plot_expenses_by_category(data):
    """Plot expenses by category. Self-explanatory."""
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
