from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from app.domain.users import IUsersApp
from app.messages import (
    CreateUserMessage, CreateUserResultMessage, DeleteUserMessage,
    DeleteUserResultMessage, GetUserMessage, GetUserResultMessage,
)


@dataclass
class ValidateException(Exception):
    errors: dict


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

        errors = msg.validate()

        if errors is not None:
            raise ValidateException(errors)

        match msg:
            case CreateUserMessage():
                return await self.app.create_user(msg)
            case DeleteUserMessage():
                return await self.app.delete_user(msg)
            case GetUserMessage():
                return await self.app.get_user(msg)
