import json
import aio_pika
from app.settings import settings

RABBITMQ_URL = settings.RABBITMQ_URL

async def publish_order_created(order_data: dict):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("orders", durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(order_data).encode(),
                content_type="application/json"
            ),
            routing_key=queue.name,
        )
