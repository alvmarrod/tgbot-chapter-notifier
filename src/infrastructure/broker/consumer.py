import json
from typing import Any, Awaitable, Callable, Optional

from aio_pika import IncomingMessage, Queue

try:
    from src.infrastructure.broker.rabbitmq import RabbitMQManager
except ModuleNotFoundError:
    from infrastructure.broker.rabbitmq import RabbitMQManager


OnMessage = Callable[[dict[str, Any]], Awaitable[None]]


class EventConsumer:
    def __init__(
        self,
        manager: RabbitMQManager,
        queue: Queue,
        callback: OnMessage,
    ) -> None:
        self._manager = manager
        self._queue = queue
        self._callback = callback
        self._consumer_tag: Optional[str] = None

    async def start(self) -> None:
        async def _on_message(message: IncomingMessage) -> None:
            async with message.process(requeue=True):
                body: dict[str, Any] = json.loads(message.body.decode())
                await self._callback(body)

        self._consumer_tag = await self._queue.consume(_on_message)

    async def stop(self) -> None:
        if self._consumer_tag is not None:
            await self._queue.cancel(self._consumer_tag)


class DeliveryErrorConsumer:
    def __init__(
        self,
        manager: RabbitMQManager,
        callback: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None:
        self._manager = manager
        self._callback = callback
        self._queue: Optional[Queue] = None
        self._consumer_tag: Optional[str] = None

    async def start(self) -> None:
        self._queue = await self._manager.declare_error_queue()

        async def _on_message(message: IncomingMessage) -> None:
            async with message.process(requeue=True):
                body: dict[str, Any] = json.loads(message.body.decode())
                if body.get("status") == "failed":
                    await self._callback(body)

        self._consumer_tag = await self._queue.consume(_on_message)

    async def stop(self) -> None:
        if self._consumer_tag is not None and self._queue is not None:
            await self._queue.cancel(self._consumer_tag)
