import uuid

import pytest
from app.store.adapter import ModelUser
from app.store.redis import RedisAdapter


# Вообще стоило было сделать три разных теста.
@pytest.mark.asyncio
async def test_adapter():
    adapter = RedisAdapter()

    result = await adapter.create_user(ModelUser(first_name='Zero', second_name='Two'))
    assert isinstance(result, uuid.UUID)

    user = await adapter.get_user(result)
    assert user.id == result
    assert user.first_name == 'Zero'
    assert user.second_name == 'Two'

    await adapter.delete_user(result)
