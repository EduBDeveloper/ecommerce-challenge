import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

def test_root_endpoint():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "API operativa"}

@patch("app.routers.product.crud.list_products", return_value=[])
def test_list_products_public_empty(mock_list):
    resp = client.get("/products/")
    assert resp.status_code == 200
    assert resp.json() == []

@patch("app.routers.product.crud.list_products", return_value=[
    {"id": 1, "name": "ProdA", "price": 9.99},
    {"id": 2, "name": "ProdB", "price": 19.50},
])
def test_list_products_public_nonempty(mock_list):
    resp = client.get("/products/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) and len(data) == 2
    assert data[0]["name"] == "ProdA" and data[0]["price"] == 9.99

@patch("app.routers.order.crud.get_order_by_id", return_value=None)
def test_get_nonexistent_order(mock_get):
    resp = client.get("/orders/123")
    assert resp.status_code == 404

@patch("app.routers.order.crud.get_order_by_id", return_value={
    "id": 5, "customer_id": 2, "created_at": "2025-08-01T12:00:00Z", "items": []
})
def test_get_existing_order(mock_get):
    resp = client.get("/orders/5")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 5 and data["customer_id"] == 2

@patch("app.routers.customer.crud.get_customer_by_id", return_value=None)
def test_get_nonexistent_customer(mock_get):
    resp = client.get("/customers/999")
    assert resp.status_code == 404

@patch("app.routers.customer.crud.get_customer_by_id", return_value={
    "id": 3, "full_name": "Alice", "email": "alice@example.com"
})
def test_get_existing_customer(mock_get):
    resp = client.get("/customers/3")
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "alice@example.com"
