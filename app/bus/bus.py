from abc import ABCMeta, abstractmethod

from app.domain.users import IUsersApp
from app.messages import (
    CreateUserMessage, CreateUserResultMessage, DeleteUserMessage,
    DeleteUserResultMessage, GetUserMessage, GetUserResultMessage,
)


class IMessageBus(metaclass=ABCMeta):

    @abstractmethod
    async def handle(self, message: CreateUserMessage | DeleteUserMessage | GetUserMessage) \
            -> CreateUserResultMessage | GetUserResultMessage | DeleteUserResultMessage:
        pass


class MessageBus(IMessageBus):

    app: IUsersApp = None

    def __init__(self, app: IUsersApp):
        self.app = app

    async def handle(self, msg: CreateUserMessage | DeleteUserMessage | GetUserMessage) \
            -> CreateUserResultMessage | GetUserResultMessage | DeleteUserResultMessage:

        msg.validate()

        match msg:
            case CreateUserMessage():
                return await self.app.create_user(msg)
            case DeleteUserMessage():
                return await self.app.delete_user(msg)
            case GetUserMessage():
                return await self.app.get_user(msg)
