"""Test to check if CLI is still working after trying to change it for API."""

import subprocess
import sys
import json
import os
import tempfile


def run_command(args, cwd=None):
    """Help to run CLI command and capture output."""
    main_path = os.path.join(os.path.dirname(__file__), "..", "cli", "cli.py")
    main_path = os.path.abspath(main_path)

    result = subprocess.run(
        [sys.executable, main_path] + args, capture_output=True, text=True, cwd=cwd
    )
    return result.stdout, result.stderr, result.returncode


def test_cli_show_budget(monkeypatch):
    """Test the show_budget CLI command."""
    with tempfile.TemporaryDirectory() as tmpdir:
        budget_file = os.path.join(tmpdir, "budget.json")
        expenses_file = os.path.join(tmpdir, "expenses.json")

        # Change the env
        monkeypatch.setenv("BUDGET_FILE", budget_file)
        monkeypatch.setenv("DATA_FILE", expenses_file)

        # Create budget
        with open(budget_file, "w", encoding="utf-8") as f:
            json.dump({"2025-07": 500.0}, f)

        # Create expenses
        with open(expenses_file, "w", encoding="utf-8") as f:
            json.dump(
                [
                    {"price": 100, "category": "food", "date": "2025-07-01"},
                    {"price": 50, "category": "transport", "date": "2025-07-15"},
                ],
                f,
            )

        #
        out, err, code = run_command(
            ["--show-budget", "--year", "2025", "--month", "7"], cwd=tmpdir
        )

        print("STDOUT:\n", out)
        print("STDERR:\n", err)

        assert code == 0
        assert code == 0
        assert "Budget for 2025-07: 500.00 PLN" in out
        assert "Expenses: 150.00 PLN" in out
        assert "Remaining: 350.00" in out
