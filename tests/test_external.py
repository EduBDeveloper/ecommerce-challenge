import pytest
from fastapi import HTTPException
from app.routers.product import get_inventory
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_get_inventory_success(monkeypatch):
    monkeypatch.setattr(
        "app.routers.product.get_inventory_for_product",
        AsyncMock(return_value={"id": 1, "stock": 5})
    )
    data = await get_inventory(1)
    assert data["id"] == 1
    assert data["stock"] == 5

@pytest.mark.asyncio
async def test_get_inventory_notfound(monkeypatch):
    monkeypatch.setattr(
        "app.routers.product.get_inventory_for_product",
        AsyncMock(return_value=None)
    )
    with pytest.raises(HTTPException) as excinfo:
        await get_inventory(99)
    assert excinfo.value.status_code == 404
