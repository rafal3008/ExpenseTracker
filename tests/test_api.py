import pytest
from fastapi.testclient import TestClient
from api.api import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_data_files(tmp_path, monkeypatch):
    """Self explanatory."""
    expenses_file = tmp_path / "expenses.json"
    budget_file = tmp_path / "budget.json"

    monkeypatch.setenv("EXPENSES_FILE", str(expenses_file))
    monkeypatch.setenv("BUDGET_FILE", str(budget_file))

    expenses_file.write_text("[]")
    budget_file.write_text("{}")

    yield

    expenses_file.write_text("[]")
    budget_file.write_text("{}")


def test_set_and_get_budget():
    """Self explanatory."""
    response = client.post(
        "/budget/", json={"year": 2025, "month": 7, "amount": 1000.0}
    )
    assert response.status_code == 200
    assert "Budget for 2025-07 set to 1000.00 PLN" in response.json()["message"]

    response = client.get("/budget/2025/7")
    data = response.json()
    assert response.status_code == 200
    assert data["budget"] == 1000.0
    assert data["spent"] == 0
    assert data["remaining"] == 1000.0
    assert data["warning"] is None


def test_add_expense_and_list():
    """Self explanatory."""
    expense = {"price": 50.0, "category": "food", "date": "2025-07-05"}
    response = client.post("/expenses/", json=expense)
    assert response.status_code == 200
    assert "Added expense: 50.00 PLN" in response.json()["message"]

    response = client.get("/expenses/")
    data = response.json()
    assert len(data) == 1
    assert data[0]["price"] == 50.0
    assert data[0]["category"] == "food"
    assert data[0]["date"] == "2025-07-05"


def test_budget_warning_when_spent_high():
    """Self explanatory."""
    client.post("/budget/", json={"year": 2025, "month": 7, "amount": 100.0})

    client.post(
        "/expenses/", json={"price": 85.0, "category": "food", "date": "2025-07-01"}
    )

    response = client.get("/budget/2025/7")
    data = response.json()
    assert response["status_code"] == 200
    assert data["warning"] is not None
    assert "80%" in data["warning"] or "80 %" in data["warning"]


def test_delete_budget():
    """Self explanatory."""
    client.post("/budget/", json={"year": 2025, "month": 7, "amount": 500.0})
    response = client.delete("/budget/2025/7")
    assert response.status_code == 200
    assert "deleted" in response.json()["message"].lower()

    response = client.get("/budget/2025/7")
    assert response.status_code == 404


def test_delete_expense():
    """Self explanatory."""
    client.post(
        "/expenses/", json={"price": 20.0, "category": "books", "date": "2025-07-01"}
    )
    response = client.delete("/expenses/0")
    assert response.status_code == 200
    assert "Deleted expense" in response.json()["message"]

    response = client.delete("/expenses/0")
    assert response.status_code == 404


def test_edit_expense():
    """Self explanatory."""
    client.post(
        "/expenses/", json={"price": 10.0, "category": "misc", "date": "2025-07-01"}
    )
    response = client.patch("/expenses/0", json={"price": 15.0, "category": "books"})
    assert response.status_code == 200
    assert "updated" in response.json()["message"]

    response = client.get("/expenses/")
    data = response.json()
    assert data[0]["price"] == 15.0
    assert data[0]["category"] == "books"


def test_clear_expenses():
    """Self explanatory."""
    client.post("/expenses/", json={"price": 30.0, "category": "food"})
    response = client.delete("/expenses/")
    assert response.status_code == 200
    assert "deleted" in response.json()["message"].lower()

    response = client.get("/expenses/")
    assert response.json() == []
