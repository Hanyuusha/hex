from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass
class ModelUser:
    first_name: str
    second_name: str
    id: UUID | None = None


class DataBaseAdapter(metaclass=ABCMeta):

    @abstractmethod
    def get_user(self, uid: UUID) -> ModelUser:
        pass

    @abstractmethod
    def create_user(self, user: ModelUser) -> UUID:
        pass

    @abstractmethod
    def delete_user(self, uid: UUID) -> None:
        pass
