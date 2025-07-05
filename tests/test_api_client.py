import pytest
from unittest.mock import patch, Mock
from cli import api_client


def test_set_budget():
    with patch("cli.api_client.requests.post") as mock_post:
        mock_post.return_value = Mock(
            status_code=200, json=lambda: {"message": "Budget set"}
        )
        response = api_client.set_budget(2025, 7, 1000)
        assert response["message"] == "Budget set"
        mock_post.assert_called_once_with(
            "http://127.0.0.1:8000/budget/",
            json={"year": 2025, "month": 7, "amount": 1000},
        )


def test_get_budget():
    with patch("cli.api_client.requests.get") as mock_get:
        mock_get.return_value = Mock(
            status_code=200, json=lambda: {"budget": 1000, "spent": 200}
        )
        response = api_client.get_budget(2025, 7)
        assert response["budget"] == 1000
        mock_get.assert_called_once_with("http://127.0.0.1:8000/budget/2025/7")


def test_delete_budget():
    with patch("cli.api_client.requests.delete") as mock_delete:
        mock_delete.return_value = Mock(
            status_code=200, json=lambda: {"message": "Budget deleted"}
        )
        response = api_client.delete_budget(2025, 7)
        assert response["message"] == "Budget deleted"


def test_add_expense():
    expense = {"price": 100, "category": "food", "date": "2025-07-05"}
    with patch("cli.api_client.requests.post") as mock_post:
        mock_post.return_value = Mock(
            status_code=200, json=lambda: {"message": "Expense added"}
        )
        response = api_client.add_expense(expense)
        assert response["message"] == "Expense added"


def test_list_expenses():
    with patch("cli.api_client.requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: [{"price": 50}])
        response = api_client.list_expenses()
        assert isinstance(response, list)
        assert response[0]["price"] == 50


def test_delete_expense():
    with patch("cli.api_client.requests.delete") as mock_delete:
        mock_delete.return_value = Mock(
            status_code=200, json=lambda: {"message": "Deleted"}
        )
        response = api_client.delete_expense(0)
        assert response["message"] == "Deleted"


def test_edit_expense():
    data = {"price": 60}
    with patch("cli.api_client.requests.patch") as mock_patch:
        mock_patch.return_value = Mock(
            status_code=200, json=lambda: {"message": "Updated"}
        )
        response = api_client.edit_expense(0, data)
        assert response["message"] == "Updated"


def test_clear_expenses():
    with patch("cli.api_client.requests.delete") as mock_delete:
        mock_delete.return_value = Mock(
            status_code=200, json=lambda: {"message": "All deleted"}
        )
        response = api_client.clear_expenses()
        assert response["message"] == "All deleted"
