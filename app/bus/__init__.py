from app.store import get_store

from .bus import IMessageBus, MessageBus, ValidateException  # noqa: F401
from .messages import CreateUserMessage, GetUserMessage  # noqa: F401


def get_message_bus() -> IMessageBus:
    return MessageBus(get_store())
