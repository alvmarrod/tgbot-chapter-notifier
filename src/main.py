"""
Chapter Notifier Telegram Bot

This bot checks for new content on certain websites to notify the user that has
previously suscribed about it.
"""
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

try:
    from src.app.client import (
        broker_config,
        BOT_ID,
        SUBSCRIBER_ID,
        INCOMING_ROUTING_KEY,
        BOT_COMMANDS,
    )
    from src.app.handlers import COMMAND_MAP, CALLBACK_MAP
    from src.app.cron import perform_search_generator
    from src.app.dispatcher import EventDispatcher
    from src.app.actions import handle_delivery_error
    from src.infrastructure.broker import (
        RabbitMQManager,
        ResponsePublisher,
        EventConsumer,
        DeliveryErrorConsumer,
    )
    from src.utils import log
except ModuleNotFoundError:
    from app.client import (
        broker_config,
        BOT_ID,
        SUBSCRIBER_ID,
        INCOMING_ROUTING_KEY,
        BOT_COMMANDS,
    )
    from app.handlers import COMMAND_MAP, CALLBACK_MAP
    from app.cron import perform_search_generator
    from app.dispatcher import EventDispatcher
    from app.actions import handle_delivery_error
    from infrastructure.broker import (
        RabbitMQManager,
        ResponsePublisher,
        EventConsumer,
        DeliveryErrorConsumer,
    )
    from utils import log


scheduler = AsyncIOScheduler()
scheduler.start()


async def main() -> None:
    log("bot", "info", ["main", "Starting bot with AMQP transport"])

    manager = RabbitMQManager(broker_config)
    await manager.connect()

    subscriber_queue = await manager.declare_subscriber_queue(
        INCOMING_ROUTING_KEY
    )

    publisher = ResponsePublisher(manager, BOT_ID)

    dispatcher = EventDispatcher(
        publisher=publisher,
        command_map=COMMAND_MAP,
        callback_map=CALLBACK_MAP,
    )

    event_consumer = EventConsumer(
        manager, subscriber_queue, dispatcher.handle_event
    )
    await event_consumer.start()

    error_consumer = DeliveryErrorConsumer(manager, handle_delivery_error)
    await error_consumer.start()

    await publisher.register_commands(
        bot_id=BOT_ID,
        subscriber_id=SUBSCRIBER_ID,
        commands=[
            {"command": c["command"], "description": c["description"]}
            for c in BOT_COMMANDS
        ],
    )
    log("bot", "info", ["main", "Bot commands registered"])

    log("bot", "info", ["main", "Running discovery for init"])
    search_fn = perform_search_generator(publisher, BOT_ID)
    await search_fn()

    scheduler.add_job(
        perform_search_generator(publisher, BOT_ID), "cron", minute="*/15"
    )

    log("bot", "info", ["main", "Bot ready. Waiting for events..."])

    try:
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        pass
    finally:
        await event_consumer.stop()
        await error_consumer.stop()
        await manager.disconnect()
        log("bot", "info", ["main", "Bot stopped"])


if __name__ == "__main__":
    asyncio.run(main())
