import uuid

import pytest

from app.store.adapter import ModelUser
from app.store.sql import SQLAlchemyAdapter, User


@pytest.fixture
def adapter():
    return SQLAlchemyAdapter()


@pytest.fixture
@pytest.mark.asyncio
async def uid(adapter):
    uid = uuid.uuid4()
    async with adapter.Session() as session:
        orm_user = User(
            id=uid,
            first_name='Zero',
            second_name='Two'
        )
        session.add(orm_user)
        await session.commit()

    return uid


@pytest.mark.asyncio
async def test_create_user(adapter):
    adapter = SQLAlchemyAdapter()
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
async def test_get_user_not_exists(adapter):
    user = await adapter.get_user(uuid.uuid4())
    assert user is None


@pytest.mark.asyncio
async def test_delete_exists_user(adapter, uid):
    uid = await uid
    exists = await adapter.delete_user(uid)
    assert exists is True


@pytest.mark.asyncio
async def test_delete_non_exists_user(adapter):
    exists = await adapter.delete_user(uuid.uuid4())
    assert exists is False
