import uuid

from fastapi import APIRouter, Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.bus import IMessageBus, get_message_bus
from app.domain import InternalException
from app.messages import (
    CreateUserMessage, DeleteUserMessage, GetUserMessage, UpdateUserMessage,
    ValidateException,
)

app = FastAPI()

rout = APIRouter(prefix='/api/v1')

bus = get_message_bus()


def get_bus():
    return bus


@app.exception_handler(InternalException)
async def internal_exception_handler(_: Request, exc: InternalException):
    return JSONResponse(
        status_code=exc.status,
        content=exc.errors,
    )


@app.exception_handler(ValidateException)
async def validation_exception_handler(_: Request, exc: ValidateException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=exc.errors,
    )


class CreateUpdateUser(BaseModel):
    first_name: str
    second_name: str


@rout.post('/user')
async def create_user(user: CreateUpdateUser, bus: IMessageBus = Depends(get_bus)):
    result = await bus.handle(
        CreateUserMessage(
            first_name=user.first_name,
            second_name=user.second_name,
        )
    )
    return result.to_json()


@rout.get('/user/{uid}')
async def get_user(uid: uuid.UUID, bus: IMessageBus = Depends(get_bus)):
    result = await bus.handle(
        GetUserMessage(
            id=uid
        )
    )
    return result.to_json()


@rout.delete('/user/{uid}')
async def del_user(uid: uuid.UUID, bus: IMessageBus = Depends(get_bus)):
    result = await bus.handle(
        DeleteUserMessage(
            id=uid
        )
    )
    return result.to_json()


@rout.patch('/user/{uid}')
async def update_user(uid: uuid.UUID, new_user_data: CreateUpdateUser, bus: IMessageBus = Depends(get_bus)):
    result = await bus.handle(
        UpdateUserMessage(
            id=uid,
            first_name=new_user_data.first_name,
            second_name=new_user_data.second_name,
        )
    )
    return result.to_json()

app.include_router(rout)
