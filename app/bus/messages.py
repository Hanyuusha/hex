from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from app.db.adapter import ModelUser


class BaseResponse(metaclass=ABCMeta):

    @abstractmethod
    def to_json(self) -> dict:
        pass


class BaseRequest(metaclass=ABCMeta):

    @abstractmethod
    def validate(self) -> None | dict:
        pass


@dataclass
class CreateUserMessage(BaseRequest):
    first_name: str
    second_name: str

    def to_user(self) -> ModelUser:
        return ModelUser(first_name=self.first_name, second_name=self.second_name)

    def validate(self) -> None | dict:
        if self.first_name is None:
            return {'message': '"first_name" not defined'}
        if self.second_name is None:
            return {'message': '"second_name" not defined'}


@dataclass
class CreateUserResultMessage(BaseResponse):
    id: UUID

    def to_json(self) -> dict:
        return {'id': self.id}


@dataclass
class GetUserMessage(BaseRequest):
    id: UUID

    def validate(self) -> None | dict:
        if self.id is None:
            return {'message': '"id" not defined'}


@dataclass
class GetUserResultMessage(BaseResponse):
    id: UUID
    first_name: str
    second_name: str

    def to_json(self):
        return {'id': self.id, 'first_name': self.first_name, 'second_name': self.second_name}


@dataclass
class DeleteUserMessage(BaseRequest):
    id: UUID

    def validate(self) -> None | dict:
        if self.id is None:
            return {'message': '"id" not defined'}
