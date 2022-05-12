import uuid

import pytest
from app.bus.bus import MessageBus
from app.bus.messages import (
    CreateUserMessage, DeleteUserMessage, GetUserMessage,
)
from app.store.adapter import TestDatabaseAdapter


@pytest.fixture
def message_bus():
    return MessageBus(adapter=TestDatabaseAdapter())


@pytest.mark.asyncio
async def test_handle_create_user(message_bus):
    msg = CreateUserMessage(first_name='Zero', second_name='Two')
    result = await message_bus.handle(msg)

    assert isinstance(result.id, uuid.UUID)


@pytest.mark.asyncio
async def test_handle_get_user(message_bus):
    uid = uuid.uuid4()
    msg = GetUserMessage(id=uid)
    result = await message_bus.handle(msg)

    assert result.id == uid
    assert result.first_name == 'Zero'
    assert result.second_name == 'Second'


@pytest.mark.asyncio
async def test_handle_delete_user(message_bus):
    msg = DeleteUserMessage(id=uuid.uuid4())
    result = await message_bus.handle(msg)

    assert result is None
