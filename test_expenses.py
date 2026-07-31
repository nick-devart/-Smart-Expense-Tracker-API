import pytest
from fastapi.testclient import TestClient
from src.main import app
from src import store
client = TestClient(app)
@pytest.fixture(autouse=True)
def reset_store():
    """Clear the in-memory store before each test."""
    store.clear()
    yield
    store.clear()
def create_expense(title="Lunch", amount=12.50, category="Food", date="2026-07-01"):
    return client.post("/expenses/", json={
        "title": title,
        "amount": amount,
        "category": category,
        "date": date,
    })
def test_add_expense_success():
    res = create_expense()
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Lunch"
    assert data["amount"] == 12.50
    assert data["category"] == "Food"
    assert data["date"] == "2026-07-01"
    assert "id" in data
def test_add_expense_missing_field():
    res = client.post("/expenses/", json={"title": "Lunch", "amount": 10.0})
    assert res.status_code == 422
def test_add_expense_negative_amount():
    res = client.post("/expenses/", json={
        "title": "Bad", "amount": -5, "category": "Other", "date": "2026-07-01"
    })
    assert res.status_code == 422
def test_add_expense_zero_amount():
    res = client.post("/expenses/", json={
        "title": "Bad", "amount": 0, "category": "Other", "date": "2026-07-01"
    })
    assert res.status_code == 422
def test_list_expenses_empty():
    res = client.get("/expenses/")
    assert res.status_code == 200
    assert res.json() == []
def test_list_expenses_returns_all():
    create_expense("Lunch", 10, "Food")
    create_expense("Bus", 2.5, "Transport")
    res = client.get("/expenses/")
    assert res.status_code == 200
    assert len(res.json()) == 2
def test_filter_by_category():
    create_expense("Lunch", 10, "Food")
    create_expense("Dinner", 20, "Food")
    create_expense("Bus", 2.5, "Transport")
    res = client.get("/expenses/?category=Food")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 2
    assert all(e["category"] == "Food" for e in data)
def test_filter_by_category_case_insensitive():
    create_expense("Lunch", 10, "Food")
    res = client.get("/expenses/?category=food")
    assert res.status_code == 200
    assert len(res.json()) == 1
def test_filter_by_category_no_match():
    create_expense("Lunch", 10, "Food")
    res = client.get("/expenses/?category=Travel")
    assert res.status_code == 200
    assert res.json() == []
def test_summary_empty():
    res = client.get("/expenses/summary")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 0
    assert data["count"] == 0
    assert data["by_category"] == []
def test_summary_overall():
    create_expense("Lunch", 10, "Food")
    create_expense("Dinner", 20, "Food")
    create_expense("Bus", 5, "Transport")
    res = client.get("/expenses/summary")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 35
    assert data["count"] == 3
    categories = {c["category"]: c for c in data["by_category"]}
    assert categories["Food"]["total"] == 30
    assert categories["Food"]["count"] == 2
    assert categories["Transport"]["total"] == 5
    assert categories["Transport"]["count"] == 1
def test_summary_by_category():
    create_expense("Lunch", 10, "Food")
    create_expense("Bus", 5, "Transport")
    res = client.get("/expenses/summary?category=Food")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 10
    assert data["count"] == 1
def test_delete_expense_success():
    created = create_expense().json()
    expense_id = created["id"]
    res = client.delete(f"/expenses/{expense_id}")
    assert res.status_code == 204
    all_expenses = client.get("/expenses/").json()
    assert all(e["id"] != expense_id for e in all_expenses)
def test_delete_nonexistent_expense():
    res = client.delete("/expenses/nonexistent-id")
    assert res.status_code == 404
def test_delete_does_not_affect_others():
    e1 = create_expense("Lunch", 10, "Food").json()
    e2 = create_expense("Bus", 5, "Transport").json()
    client.delete(f"/expenses/{e1['id']}")
    remaining = client.get("/expenses/").json()
    assert len(remaining) == 1
    assert remaining[0]["id"] == e2["id"]
