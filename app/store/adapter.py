from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class ModelUser:
    first_name: str
    second_name: str
    id: UUID | None = None

    def to_json(self) -> dict:
        return {'id': str(self.id), 'first_name': self.first_name, 'second_name': self.second_name}


class DataBaseAdapter(metaclass=ABCMeta):

    @abstractmethod
    async def get_user(self, uid: UUID) -> ModelUser:
        pass

    @abstractmethod
    async def create_user(self, user: ModelUser) -> UUID:
        pass

    @abstractmethod
    async def delete_user(self, uid: UUID) -> None:
        pass


class TestDatabaseAdapter(DataBaseAdapter):

    async def create_user(self, user: ModelUser) -> UUID:
        return uuid4()

    async def delete_user(self, uid: UUID) -> None:
        return None

    async def get_user(self, uid: UUID) -> ModelUser:
        return ModelUser(id=uid, first_name='Zero', second_name='Second')
