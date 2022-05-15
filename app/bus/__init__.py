from app.domain import get_domain_app

from .bus import IMessageBus, MessageBus, ValidateException  # noqa: F401


def get_message_bus() -> IMessageBus:
    return MessageBus(get_domain_app())
