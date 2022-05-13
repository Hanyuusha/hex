import json
import uuid

import pytest
from app.store.adapter import ModelUser
from app.store.redis import RedisAdapter


@pytest.fixture
def adapter() -> RedisAdapter:
    return RedisAdapter()


@pytest.fixture
@pytest.mark.asyncio
async def uid(adapter):
    uid = uuid.uuid4()
    await adapter.redis.set(str(uid), json.dumps(ModelUser(id=uid, first_name='Zero', second_name='Two').to_json()))
    return uid


# Вообще стоило было сделать три разных теста.
@pytest.mark.asyncio
async def test_create_user(adapter):
    result = await adapter.create_user(ModelUser(first_name='Zero', second_name='Two'))
    assert isinstance(result, uuid.UUID)


@pytest.mark.asyncio
async def test_get_user(adapter, uid):
    uid = await uid
    user = await adapter.get_user(uid)
    assert user.id == uid
    assert user.first_name == 'Zero'
    assert user.second_name == 'Two'


@pytest.mark.asyncio
async def test_delete_exists_user(adapter, uid):
    uid = await uid
    exists = await adapter.delete_user(uid)
    assert exists is True


@pytest.mark.asyncio
async def test_delete_non_exists_user(adapter):
    exists = await adapter.delete_user(uuid.uuid4())
    assert exists is False
