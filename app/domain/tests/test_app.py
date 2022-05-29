import uuid
from unittest.mock import patch

import pytest

from app.domain.users import InternalException, UserApp
from app.messages import CreateUserMessage, DeleteUserMessage, GetUserMessage
from app.store.adapter import ModelUser


@pytest.mark.asyncio
@patch('app.store.adapter.DataBaseAdapter')
@patch('app.store.adapter.DataBaseAdapter.create_user')
async def test_handle_create_user(mock_create_user, mock_database_adapter):
    uid = uuid.uuid4()
    mock_create_user.return_value = uid
    mock_database_adapter.return_value.create_user = mock_create_user

    user_app = UserApp(adapter=mock_database_adapter())
    msg = CreateUserMessage(first_name='Zero', second_name='Two')
    result = await user_app.create_user(msg)

    assert result.id == uid


@pytest.mark.asyncio
@patch('app.store.adapter.DataBaseAdapter')
@patch('app.store.adapter.DataBaseAdapter.get_user')
async def test_handle_get_user(mock_get_user, mock_database_adapter):
    uid = uuid.uuid4()
    first_name = 'Zero'
    second_name = 'Two'
    result = ModelUser(id=uid, first_name=first_name, second_name=second_name)
    mock_get_user.return_value = result
    mock_database_adapter.return_value.get_user = mock_get_user

    user_app = UserApp(adapter=mock_database_adapter())
    msg = GetUserMessage(id=uid)
    result = await user_app.get_user(msg)

    assert result.id == uid
    assert result.first_name == 'Zero'
    assert result.second_name == 'Two'


@pytest.mark.asyncio
@patch('app.store.adapter.DataBaseAdapter')
@patch('app.store.adapter.DataBaseAdapter.get_user')
async def test_handle_get_user_not_found(mock_get_user, mock_database_adapter):
    mock_get_user.return_value = None
    mock_database_adapter.return_value.get_user = mock_get_user

    user_app = UserApp(adapter=mock_database_adapter())
    msg = GetUserMessage(id=uuid.uuid4())
    with pytest.raises(InternalException) as exc:
        await user_app.get_user(msg)
    assert exc.value.status == 404


@pytest.mark.asyncio
@patch('app.store.adapter.DataBaseAdapter')
@patch('app.store.adapter.DataBaseAdapter.delete_user')
async def test_handle_delete_user(mock_delete_user, mock_database_adapter):
    msg = DeleteUserMessage(id=uuid.uuid4())

    mock_delete_user.return_value = True
    mock_database_adapter.return_value.delete_user = mock_delete_user

    user_app = UserApp(adapter=mock_database_adapter())
    result = await user_app.delete_user(msg)

    assert result.exists is True
