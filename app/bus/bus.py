from abc import ABCMeta, abstractmethod

from app.store.adapter import DataBaseAdapter

from .messages import (
    CreateUserMessage, CreateUserResultMessage, DeleteUserMessage,
    GetUserMessage, GetUserResultMessage, DeleteUserResultMessage,
)


class InternalException(Exception):
    errors: dict
    status: int

    def __init__(self, errors, status=400):
        self.errors = errors
        self.status = status


class IMessageBus(metaclass=ABCMeta):

    @abstractmethod
    async def handle(self, message: CreateUserMessage | DeleteUserMessage | GetUserMessage) \
            -> CreateUserResultMessage | GetUserResultMessage | DeleteUserResultMessage:
        pass


class MessageBus(IMessageBus):

    adapter: DataBaseAdapter = None

    def __init__(self, adapter: DataBaseAdapter):
        self.adapter = adapter

    async def handle(self, msg: CreateUserMessage | DeleteUserMessage | GetUserMessage) \
            -> CreateUserResultMessage | GetUserResultMessage | DeleteUserResultMessage:

        errors = msg.validate()

        if errors is not None:
            raise InternalException(errors)

        match msg:
            case CreateUserMessage():
                return await self.create_user(msg)
            case DeleteUserMessage():
                return await self.delete_user(msg)
            case GetUserMessage():
                return await self.get_user(msg)

    async def create_user(self, msg: CreateUserMessage) -> CreateUserResultMessage:
        uid = await self.adapter.create_user(msg.to_user())
        return CreateUserResultMessage(id=uid)

    async def delete_user(self, msg):
        exists = await self.adapter.delete_user(msg.id)
        return DeleteUserResultMessage(exists=exists)

    async def get_user(self, msg: GetUserMessage) -> GetUserResultMessage:
        user = await self.adapter.get_user(msg.id)

        if user is None:
            raise InternalException({'message': 'user not found'}, status=404)

        return GetUserResultMessage(id=user.id, first_name=user.first_name, second_name=user.second_name)
