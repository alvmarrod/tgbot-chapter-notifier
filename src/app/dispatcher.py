from typing import Any, Optional, Callable, Awaitable

from src.infrastructure.broker import ResponsePublisher

Handler = Callable[..., Awaitable[None]]


class Responder:
    def __init__(
        self,
        publisher: ResponsePublisher,
        chat_id: int,
        message_id: Optional[int] = None,
        callback_id: Optional[str] = None,
        reply_to: Optional[str] = None,
    ) -> None:
        self._publisher = publisher
        self.chat_id = chat_id
        self.message_id = message_id
        self.callback_id = callback_id
        self._reply_to = reply_to

    async def reply_text(
        self,
        text: str,
        parse_mode: Optional[str] = None,
        reply_markup: Optional[list[list[dict[str, str]]]] = None,
    ) -> None:
        await self._publisher.publish_text(
            chat_id=self.chat_id,
            text=text,
            parse_mode=parse_mode,
            reply_to_message_id=self.message_id,
            reply_markup=reply_markup,
        )

    async def send_message(
        self,
        chat_id: int,
        text: str,
        parse_mode: Optional[str] = None,
        reply_markup: Optional[list[list[dict[str, str]]]] = None,
        disable_web_page_preview: Optional[bool] = None,
    ) -> None:
        await self._publisher.publish_text(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            disable_web_page_preview=disable_web_page_preview,
        )

    async def edit_text(
        self,
        text: str,
        parse_mode: Optional[str] = None,
        reply_markup: Optional[list[list[dict[str, str]]]] = None,
    ) -> None:
        await self._publisher.publish_edit(
            chat_id=self.chat_id,
            message_id=self.message_id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
        )

    async def answer_callback(
        self,
        text: Optional[str] = None,
        show_alert: bool = False,
    ) -> None:
        await self._publisher.publish_callback_answer(
            callback_query_id=self.callback_id,
            text=text,
            show_alert=show_alert,
        )

    def with_reply_to(self, reply_to: str) -> "Responder":
        return Responder(
            publisher=self._publisher,
            chat_id=self.chat_id,
            message_id=self.message_id,
            callback_id=self.callback_id,
            reply_to=reply_to,
        )


class EventDispatcher:
    def __init__(
        self,
        publisher: ResponsePublisher,
        command_map: dict[str, Handler],
        callback_map: dict[str, Handler],
    ) -> None:
        self._publisher = publisher
        self._command_map = command_map
        self._callback_map = callback_map

    async def handle_event(self, envelope: dict[str, Any]) -> None:
        event_type = envelope.get("event_type", "")
        chat_id = envelope.get("chat_id", 0)
        user_id = envelope.get("user_id", 0)
        message_id: Optional[int] = envelope.get("message_id")
        payload = envelope.get("payload", {})
        routing_context = envelope.get("routing_context", {})

        if event_type == "command":
            command = routing_context.get("command", "")
            handler = self._command_map.get(command)
            if handler is None:
                return
            responder = Responder(
                publisher=self._publisher,
                chat_id=chat_id,
                message_id=message_id,
            )
            await handler(
                responder=responder,
                chat_id=chat_id,
                user_id=user_id,
                message_id=message_id,
            )

        elif event_type == "callback_query":
            callback_data = envelope.get("callback_data", "")
            callback_id = envelope.get("callback_id", "")
            caller = callback_data.split(":")[0] if callback_data else ""
            handler = self._callback_map.get(caller)
            if handler is None:
                return
            responder = Responder(
                publisher=self._publisher,
                chat_id=chat_id,
                message_id=message_id,
                callback_id=callback_id,
            )
            await handler(
                responder=responder,
                chat_id=chat_id,
                user_id=user_id,
                callback_data=callback_data,
                callback_id=callback_id,
                message_id=message_id,
            )
