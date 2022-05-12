from abc import ABCMeta, abstractmethod

from .messages import CreateUserMessage, DeleteUserMessage, GetUserMessage, CreateUserResultMessage, GetUserResultMessage
from app.db.adapter import DataBaseAdapter


class IMessageBus(metaclass=ABCMeta):

    @abstractmethod
    async def handle(self, message: CreateUserMessage | DeleteUserMessage | GetUserMessage) \
            -> CreateUserResultMessage | GetUserResultMessage | None:
        pass


class MessageBus(IMessageBus):

    adapter: DataBaseAdapter = None

    def __init__(self, adapter: DataBaseAdapter):
        self.adapter = adapter

    async def handle(self, message: CreateUserMessage | DeleteUserMessage | GetUserMessage) \
            -> CreateUserResultMessage | GetUserResultMessage | None:
        match message:
            case CreateUserMessage():
                uid = await self.adapter.create_user(message.to_user())
                return CreateUserResultMessage(id=uid)
            case DeleteUserMessage():
                return await self.adapter.delete_user(message.id)
            case GetUserMessage():
                user = await self.adapter.get_user(message.id)
                return GetUserResultMessage(id=user.id, first_name=user.first_name, second_name=user.second_name)
