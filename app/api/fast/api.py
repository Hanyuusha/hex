import uuid

from app.bus import (
    CreateUserMessage, GetUserMessage, IMessageBus, get_message_bus, ValidateException,
)
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class CreateUser(BaseModel):
    first_name: str
    second_name: str


@app.post("/api/v1/user")
async def create_user(user: CreateUser, bus: IMessageBus = Depends(get_message_bus)):
    result = await bus.handle(
        CreateUserMessage(
            first_name=user.first_name,
            second_name=user.second_name,
        )
    )
    return result.to_json()


@app.get("/api/v1/user/{uid}")
async def get_user(uid: uuid.UUID, bus: IMessageBus = Depends(get_message_bus)):
    result = None
    try:
        result = await bus.handle(
            GetUserMessage(
                id=uid
            )
        )
    except ValidateException as e:
        raise HTTPException(status_code=404, detail=e.errors)
    return result.to_json()
