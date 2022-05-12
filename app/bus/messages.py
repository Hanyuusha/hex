from dataclasses import dataclass
from uuid import UUID

from app.db.adapter import ModelUser


@dataclass
class CreateUserMessage:
    first_name: str
    second_name: str

    def to_user(self) -> ModelUser:
        return ModelUser(first_name=self.first_name, second_name=self.second_name)


@dataclass
class CreateUserResultMessage:
    id: UUID


@dataclass
class GetUserMessage:
    id: UUID


@dataclass
class GetUserResultMessage:
    id: UUID
    first_name: str
    second_name: str


@dataclass
class DeleteUserMessage:
    id: UUID
