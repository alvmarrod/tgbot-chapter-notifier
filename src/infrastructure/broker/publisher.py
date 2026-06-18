import json
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

import aio_pika

from src.infrastructure.broker.rabbitmq import RabbitMQManager


class ResponsePublisher:
    def __init__(self, manager: RabbitMQManager, bot_id: str) -> None:
        self._manager = manager
        self._bot_id = bot_id
        self._responses_exchange: Optional[aio_pika.Exchange] = None

    async def _ensure_exchange(self) -> aio_pika.Exchange:
        if self._responses_exchange is None:
            self._responses_exchange = await self._manager.get_exchange(
                "tg-if.responses", "direct"
            )
        return self._responses_exchange

    async def publish_response(
        self,
        response_type: str,
        chat_id: int,
        payload: dict[str, Any],
        correlation_id: str = "",
        reply_to: Optional[str] = None,
    ) -> None:
        exchange = await self._ensure_exchange()
        envelope = {
            "response_id": str(uuid.uuid4()),
            "correlation_id": correlation_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "bot_id": self._bot_id,
            "chat_id": chat_id,
            "response_type": response_type,
            "payload": payload,
        }
        if reply_to:
            envelope["reply_to"] = reply_to

        await exchange.publish(
            aio_pika.Message(
                body=json.dumps(envelope).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key="response",
        )

    async def publish_text(
        self,
        chat_id: int,
        text: str,
        parse_mode: Optional[str] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[list[list[dict[str, str]]]] = None,
        disable_web_page_preview: Optional[bool] = None,
        reply_to: Optional[str] = None,
    ) -> None:
        payload: dict[str, Any] = {"text": text}
        if parse_mode:
            payload["parse_mode"] = parse_mode
        if reply_to_message_id is not None:
            payload["reply_to_message_id"] = reply_to_message_id
        if reply_markup is not None:
            payload["reply_markup"] = reply_markup
        if disable_web_page_preview is not None:
            payload["disable_web_page_preview"] = disable_web_page_preview
        await self.publish_response("text", chat_id, payload, reply_to=reply_to)

    async def publish_edit(
        self,
        chat_id: int,
        message_id: int,
        text: str,
        parse_mode: Optional[str] = None,
        reply_markup: Optional[list[list[dict[str, str]]]] = None,
    ) -> None:
        payload: dict[str, Any] = {"message_id": message_id, "text": text}
        if parse_mode:
            payload["parse_mode"] = parse_mode
        if reply_markup is not None:
            payload["reply_markup"] = reply_markup
        await self.publish_response("edit_message_text", chat_id, payload)

    async def publish_callback_answer(
        self,
        callback_query_id: str,
        text: Optional[str] = None,
        show_alert: bool = False,
    ) -> None:
        payload: dict[str, Any] = {"callback_query_id": callback_query_id}
        if text is not None:
            payload["text"] = text
        if show_alert:
            payload["show_alert"] = show_alert
        envelope = {
            "response_id": str(uuid.uuid4()),
            "correlation_id": "",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "bot_id": self._bot_id,
            "response_type": "answer_callback_query",
            "payload": payload,
        }
        exchange = await self._ensure_exchange()
        await exchange.publish(
            aio_pika.Message(
                body=json.dumps(envelope).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key="response",
        )

    async def register_commands(
        self,
        bot_id: str,
        subscriber_id: str,
        commands: list[dict[str, str]],
    ) -> None:
        exchange = await self._ensure_exchange()
        envelope = {
            "action": "register",
            "bot_id": bot_id,
            "subscriber_id": subscriber_id,
            "commands": commands,
        }
        await exchange.publish(
            aio_pika.Message(
                body=json.dumps(envelope).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key="subscriber-commands",
        )
