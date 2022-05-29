import uuid

import pytest

from app.messages import (
    CreateUserMessage, CreateUserResultMessage, DeleteUserMessage,
    DeleteUserResultMessage, GetUserMessage, GetUserResultMessage,
    ValidateException,
)
from app.store.adapter import ModelUser


def test_create_user_message_to_user():
    first_name = 'Zero'
    second_name = 'Two'
    msg = CreateUserMessage(first_name=first_name, second_name=second_name)
    user = msg.to_user()
    assert isinstance(user, ModelUser)
    assert user.first_name == first_name
    assert user.second_name == second_name


def test_create_user_message_validate_first_name():
    msg = CreateUserMessage(first_name=None, second_name='Two')
    with pytest.raises(ValidateException) as exc:
        msg.validate()
    assert exc.value.errors['message'] == '"first_name" not defined'


def test_create_user_message_validate_second_name():
    msg = CreateUserMessage(first_name='Zero', second_name=None)
    with pytest.raises(ValidateException) as exc:
        msg.validate()
    assert exc.value.errors['message'] == '"second_name" not defined'


def test_create_user_result_message():
    uid = uuid.uuid4()
    msg = CreateUserResultMessage(id=uid)
    payload = msg.to_json()
    assert payload['id'] == uid


def test_get_user_message_validate():
    msg = GetUserMessage(id=None)
    with pytest.raises(ValidateException) as exc:
        msg.validate()
    assert exc.value.errors['message'] == '"id" not defined'


def test_get_user_result_message():
    uid = uuid.uuid4()
    first_name = 'Zero'
    second_name = 'Two'
    msg = GetUserResultMessage(id=uid, first_name=first_name, second_name=second_name)
    payload = msg.to_json()
    assert payload['id'] == uid
    assert payload['first_name'] == first_name
    assert payload['second_name'] == second_name


def test_delete_user_message_validate():
    msg = DeleteUserMessage(id=None)
    with pytest.raises(ValidateException) as exc:
        msg.validate()
    assert exc.value.errors['message'] == '"id" not defined'


def test_delete_user_message_result():
    msg = DeleteUserResultMessage(exists=True)
    payload = msg.to_json()
    assert payload['exists'] is True
