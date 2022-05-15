from asgiref.wsgi import WsgiToAsgi
from fastapi import status
from flask import Flask, request
from flask.views import MethodView

from app.bus import IMessageBus, get_message_bus
from app.domain import InternalException
from app.messages import (
    CreateUserMessage, DeleteUserMessage, GetUserMessage, ValidateException,
)

app = Flask(__name__)


class UserAPI(MethodView):

    message_bus: IMessageBus = None

    def __init__(self):
        self.message_bus = get_message_bus()

    async def get(self, uid):
        result = await self.message_bus.handle(
            GetUserMessage(
                id=uid
            )
        )

        return result.to_json()

    async def post(self):
        payload = request.json

        result = await self.message_bus.handle(
            CreateUserMessage(
                first_name=payload.get('first_name'),
                second_name=payload.get('second_name')
            )
        )

        return result.to_json()

    async def delete(self, uid):
        result = await self.message_bus.handle(
            DeleteUserMessage(
                id=uid
            )
        )

        return result.to_json()


@app.errorhandler(InternalException)
def internal_exception_handler(exc: InternalException):
    return exc.errors, exc.status


@app.errorhandler(ValidateException)
def validate_exception_handler(exc: ValidateException):
    return exc.errors, status.HTTP_400_BAD_REQUEST


user_view = UserAPI.as_view('user_api')
app.add_url_rule('/api/v1/user/<uuid:uid>', view_func=user_view, methods=['GET', 'DELETE'])
app.add_url_rule('/api/v1/user', view_func=user_view, methods=['POST'])

asgi_app = WsgiToAsgi(app)
