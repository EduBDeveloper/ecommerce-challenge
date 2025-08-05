import pytest
from app.queue import publish_order_created
import aio_pika
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_publish_order_created(monkeypatch):
    # Mocks de conexión y canal
    mock_conn = AsyncMock()
    mock_channel = AsyncMock()
    mock_queue = AsyncMock()

    monkeypatch.setattr(aio_pika, "connect_robust", AsyncMock(return_value=mock_conn))
    mock_conn.__aenter__.return_value = mock_conn
    mock_conn.channel.return_value = mock_channel
    mock_channel.declare_queue.return_value = mock_queue
    mock_channel.default_exchange.publish = AsyncMock()

    data = {
        "order_id": 1,
        "customer_id": 1,
        "items": [{"product_id": 1, "quantity": 1}]
    }

    await publish_order_created(data)

    mock_channel.default_exchange.publish.assert_called_once()
