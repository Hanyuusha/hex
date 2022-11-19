import uuid
from unittest.mock import patch

import pytest

from app.bus import MessageBus
from app.messages import (
    CreateUserMessage, CreateUserResultMessage, DeleteUserMessage,
    DeleteUserResultMessage, GetUserMessage, GetUserResultMessage,
    UpdateUserMessage, UpdateUserResultMessage,
)


@patch('app.domain.users.UserApp')
@patch('app.domain.users.UserApp.get_user')
@pytest.mark.asyncio
async def test_handle_get_user(mock_get_user, mock_user_app):
    uid = uuid.uuid4()
    first_name = 'Zero'
    second_name = 'Two'
    return_value = GetUserResultMessage(id=uid, first_name=first_name, second_name=second_name)

    message_bus = MessageBus(mock_user_app())
    mock_get_user.return_value = return_value
    mock_user_app.return_value.get_user = mock_get_user

    msg = GetUserMessage(id=uid)
    result = await message_bus.handle(msg)

    assert result.id == uid
    assert result.first_name == first_name
    assert result.second_name == second_name


@patch('app.domain.users.UserApp')
@patch('app.domain.users.UserApp.create_user')
@pytest.mark.asyncio
async def test_handle_create_user(mock_create_user, mock_user_app):
    uid = uuid.uuid4()
    mock_create_user.return_value = CreateUserResultMessage(id=uid)
    mock_user_app.return_value.create_user = mock_create_user

    message_bus = MessageBus(mock_user_app())
    msg = CreateUserMessage(first_name='Zero', second_name='Two')
    result = await message_bus.handle(msg)

    assert result.id == uid


@patch('app.domain.users.UserApp')
@patch('app.domain.users.UserApp.delete_user')
@pytest.mark.asyncio
async def test_handle_delete_user(mock_delete_user, mock_user_app):
    uid = uuid.uuid4()
    mock_delete_user.return_value = DeleteUserResultMessage(exists=True)
    mock_user_app.return_value.delete_user = mock_delete_user

    message_bus = MessageBus(mock_user_app())
    msg = DeleteUserMessage(uid)
    result = await message_bus.handle(msg)

    assert result.exists is True


@patch('app.domain.users.UserApp')
@patch('app.domain.users.UserApp.update_user')
@pytest.mark.asyncio
async def test_handle_update_user(mock_update_user, mock_user_app):
    mock_update_user.return_value = UpdateUserResultMessage()
    mock_user_app.return_value.update_user = mock_update_user

    message_bus = MessageBus(mock_user_app())
    msg = UpdateUserMessage(id=uuid.uuid4(), first_name='Rika')
    result = await message_bus.handle(msg)

    assert isinstance(result, UpdateUserResultMessage)
