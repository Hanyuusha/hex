import uuid
import pytest
from app.db.adapter import ModelUser
from app.db.sql import SQLAlchemyAdapter


# Вообще стоило было сделать три разных теста.
@pytest.mark.asyncio
async def test_adapter():
    adapter = SQLAlchemyAdapter()
    result = await adapter.create_user(ModelUser(first_name='Zero', second_name='Two'))
    assert isinstance(result, uuid.UUID)

    user = await adapter.get_user(result)
    assert user.first_name == 'Zero'
    assert user.second_name == 'Two'
    assert user.id == result

    await adapter.delete_user(result)
