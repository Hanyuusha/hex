from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass
class ModelUser:
    first_name: str
    second_name: str
    id: UUID | None = None

    def to_json(self) -> dict:
        return {'id': str(self.id), 'first_name': self.first_name, 'second_name': self.second_name}


class DataBaseAdapter(metaclass=ABCMeta):

    @abstractmethod
    async def get_user(self, uid: UUID) -> ModelUser | None:
        pass

    @abstractmethod
    async def create_user(self, user: ModelUser) -> UUID:
        pass

    @abstractmethod
    async def delete_user(self, uid: UUID) -> bool:
        pass

    @abstractmethod
    async def update_user(self, uid: UUID, payload: dict):
        pass
