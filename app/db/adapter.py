from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from uuid import UUID, uuid4


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


class TestDatabaseAdapter(DataBaseAdapter):

    def create_user(self, user: ModelUser) -> UUID:
        return uuid4()

    def delete_user(self, uid: UUID) -> None:
        return None

    def get_user(self, uid: UUID) -> ModelUser:
        return ModelUser(id=uid, first_name='Zero', second_name='Second')
