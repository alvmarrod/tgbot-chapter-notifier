import uuid
from typing import Optional

import aio_pika
from aio_pika import RobustConnection, Channel, Queue

from src.infrastructure.broker.config import BrokerConfig


class RabbitMQManager:
    def __init__(self, config: BrokerConfig) -> None:
        self._config = config
        self._connection: Optional[RobustConnection] = None
        self._channel: Optional[Channel] = None

    async def connect(self) -> None:
        self._connection = await aio_pika.connect_robust(self._config.amqp_url())
        self._channel = await self._connection.channel()

    async def declare_subscriber_queue(
        self,
        routing_key: str,
        queue_name: Optional[str] = None,
    ) -> Queue:
        queue = await self._channel.declare_queue(
            name=queue_name or f"subscriber.{uuid.uuid4().hex[:8]}",
            durable=True,
        )
        exchange = await self._channel.declare_exchange(
            "tg-if.events",
            aio_pika.ExchangeType.TOPIC,
            durable=True,
        )
        await queue.bind(exchange, routing_key=routing_key)
        return queue

    async def declare_error_queue(self) -> Queue:
        queue = await self._channel.declare_queue(
            "chaptnotifier.delivery.errors",
            durable=True,
        )
        return queue

    async def get_exchange(self, name: str, exchange_type: str) -> aio_pika.Exchange:
        type_map = {
            "topic": aio_pika.ExchangeType.TOPIC,
            "direct": aio_pika.ExchangeType.DIRECT,
        }
        return await self._channel.declare_exchange(
            name,
            type_map.get(exchange_type, aio_pika.ExchangeType.DIRECT),
            durable=True,
        )

    @property
    def channel(self) -> Channel:
        assert self._channel is not None, "Not connected"
        return self._channel

    async def disconnect(self) -> None:
        if self._connection:
            await self._connection.close()

    async def __aenter__(self) -> "RabbitMQManager":
        await self.connect()
        return self

    async def __aexit__(self, *args) -> None:
        await self.disconnect()
