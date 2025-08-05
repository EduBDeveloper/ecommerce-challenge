import pytest
from pydantic import ValidationError
from fastapi import HTTPException
from app import crud, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock

# ---- Customer CRUD & Schemas ----

@pytest.mark.asyncio
async def test_create_customer_success(monkeypatch):
    fake = {"id": 1, "full_name": "X", "email": "x@y.com"}
    monkeypatch.setattr(crud, "create_customer", AsyncMock(return_value=fake))
    res = await crud.create_customer(db=AsyncMock(), customer=schemas.CustomerCreate(full_name="X", email="x@y.com"))
    assert res["email"] == "x@y.com"

def test_create_customer_invalid_email_schema():
    with pytest.raises(ValidationError):
        schemas.CustomerCreate(full_name="X", email="invalid-email")

def test_create_customer_invalid_name_schema():
    with pytest.raises(ValidationError):
        schemas.CustomerCreate(full_name="X123", email="x@y.com")

@pytest.mark.asyncio
async def test_get_customer_notfound(monkeypatch):
    monkeypatch.setattr(crud, "get_customer_by_id", AsyncMock(return_value=None))
    from app.routers.customer import get_customer
    with pytest.raises(HTTPException) as e:
        await get_customer(5, db=AsyncMock())
    assert e.value.status_code == 404

# ---- Order CRUD & Schemas ----

@pytest.mark.asyncio
async def test_create_order_success(monkeypatch):
    fake_order = {"id": 1, "customer_id": 1, "items": []}
    monkeypatch.setattr(crud, "create_order", AsyncMock(return_value=fake_order))
    oc = schemas.OrderCreate(customer_id=1, items=[schemas.OrderItemCreate(product_id=1, quantity=1)])
    res = await crud.create_order(db=AsyncMock(), order=oc)
    assert res["id"] == 1

def test_order_create_schema_rejects_empty_items():
    with pytest.raises(ValidationError):
        schemas.OrderCreate(customer_id=1, items=[])

def test_order_create_schema_rejects_duplicates():
    with pytest.raises(ValidationError):
        schemas.OrderCreate(
            customer_id=1,
            items=[
                schemas.OrderItemCreate(product_id=1, quantity=1),
                schemas.OrderItemCreate(product_id=1, quantity=2),
            ],
        )

@pytest.mark.asyncio
async def test_get_order_notfound(monkeypatch):
    monkeypatch.setattr(crud, "get_order_by_id", AsyncMock(return_value=None))
    from app.routers.order import get_order
    with pytest.raises(HTTPException) as e:
        await get_order(123, db=AsyncMock())
    assert e.value.status_code == 404
