import uuid
from unittest.mock import patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.api.fast.api import app
from app.domain import InternalException
from app.messages import (
    CreateUserResultMessage, DeleteUserResultMessage, GetUserResultMessage,
    UpdateUserResultMessage, ValidateException,
)


@pytest.fixture
def client():
    return TestClient(app)


@patch('app.bus.bus.MessageBus.handle')
def test_get_user_ok(mock_handle, client):
    uid = uuid.uuid4()
    first_name = 'Zero'
    second_name = 'Two'
    mock_handle.return_value = GetUserResultMessage(id=uid, first_name=first_name, second_name=second_name)
    response = client.get(f'/api/v1/user/{uid}')

    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert json_response['id'] == str(uid)
    assert json_response['first_name'] == first_name
    assert json_response['second_name'] == second_name


@patch('app.bus.bus.MessageBus.handle')
def test_get_user_not_found(mock_handle, client):
    uid = uuid.uuid4()
    mock_handle.side_effect = InternalException({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
    response = client.get(f'/api/v1/user/{uid}')

    assert response.status_code == status.HTTP_404_NOT_FOUND


@patch('app.bus.bus.MessageBus.handle')
def test_user_create_ok(mock_handle, client):
    uid = uuid.uuid4()
    mock_handle.return_value = CreateUserResultMessage(id=uid)
    response = client.post('/api/v1/user', json={'first_name': 'Zero', 'second_name': 'Two'})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == str(uid)


@patch('app.bus.bus.MessageBus.handle')
def test_user_create_failed(mock_handle, client):
    mock_handle.side_effect = ValidateException(errors={}, )
    response = client.post('/api/v1/user', json={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@patch('app.bus.bus.MessageBus.handle')
def test_user_delete_ok(mock_handle, client):
    mock_handle.return_value = DeleteUserResultMessage(exists=True)
    response = client.delete(f'/api/v1/user/{uuid.uuid4()}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['exists'] is True


@patch('app.bus.bus.MessageBus.handle')
def test_user_update(mock_handle, client):
    mock_handle.return_value = UpdateUserResultMessage()
    response = client.patch(f'/api/v1/user/{uuid.uuid4()}', json={'first_name': 'Rika', 'second_name': 'Nipa'})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['updated'] is True


@patch('app.bus.bus.MessageBus.handle')
def test_exception_handler(mock_handle, client):
    mock_handle.side_effect = ValidateException(errors={'test': 'test'})
    response = client.delete(f'/api/v1/user/{uuid.uuid4()}')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['test'] == 'test'
