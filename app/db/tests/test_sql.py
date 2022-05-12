import uuid
import pytest
from app.db.adapter import ModelUser
from app.db.sql import SQLAlchemyAdapter


@pytest.fixture
def adapter():
    return SQLAlchemyAdapter()


# Вообще стоило было сделать три разных теста.
def test_adapter(adapter):

    result = adapter.create_user(ModelUser(first_name='Zero', second_name='Two'))
    assert isinstance(result, uuid.UUID)

    user = adapter.get_user(result)
    assert user.first_name == 'Zero'
    assert user.second_name == 'Two'
    assert user.id == result

    adapter.delete_user(result)
