import pytest
from click.testing import CliRunner
import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_set_budget_cli(runner):
    result = runner.invoke(cli.cli, ["set-budget", "2025", "7", "1000"])
    assert result.exit_code == 0
    assert "Budget for 2025-07 set to" in result.output


def test_get_budget_cli(runner):
    runner.invoke(cli.cli, ["set-budget", "2025", "7", "500"])
    result = runner.invoke(cli.cli, ["get-budget", "2025", "7"])
    assert result.exit_code == 0
    assert "Budget for 2025-07:" in result.output


def test_delete_budget_cli(runner):
    runner.invoke(cli.cli, ["set-budget", "2025", "7", "300"])
    result = runner.invoke(cli.cli, ["delete-budget", "2025", "7"])
    assert result.exit_code == 0
    assert "deleted" in result.output


def test_add_expense_cli(runner):
    result = runner.invoke(
        cli.cli,
        ["add-expense", "--price", "100", "--category", "food", "--date", "2025-07-05"],
    )
    assert result.exit_code == 0
    assert "Added expense" in result.output


def test_list_expenses_cli(runner):
    runner.invoke(
        cli.cli,
        ["add-expense", "--price", "50", "--category", "books", "--date", "2025-07-05"],
    )
    result = runner.invoke(cli.cli, ["list-expenses"])
    assert result.exit_code == 0
    assert "50.00 PLN" in result.output


def test_delete_expense_cli(runner):
    runner.invoke(cli, ["add-expense", "--price", "20", "--category", "misc"])
    result = runner.invoke(cli, ["delete-expense", "0"])
    assert result.exit_code == 0
    assert "Deleted expense 0" in result.output


def test_edit_expense_cli(runner):
    runner.invoke(cli, ["add-expense", "--price", "30", "--category", "travel"])
    result = runner.invoke(
        cli, ["edit-expense", "0", "--price", "35", "--category", "transport"]
    )
    assert result.exit_code == 0
    assert "Updated expense 0" in result.output


def test_clear_expenses_cli(runner):
    runner.invoke(cli, ["add-expense", "--price", "10", "--category", "misc"])
    result = runner.invoke(cli, ["clear-expenses"])
    assert result.exit_code == 0
    assert "deleted" in result.output
