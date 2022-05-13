from app.bus import CreateUserMessage, GetUserMessage, DeleteUserMessage, InternalException
from flask import Blueprint, abort, current_app, make_response, request

api = Blueprint('api', __name__)


@api.route('/user', methods=['POST'])
async def create_user():
    payload = request.json

    try:
        result = await current_app.bus.handle(
            CreateUserMessage(
                first_name=payload.get('first_name'),
                second_name=payload.get('second_name')
            )
        )
    except InternalException as e:
        abort(make_response(e.errors), 400)

    return result.to_json()


@api.route('/user/<uuid:uid>', methods=['GET'])
async def get_user(uid):
    try:
        result = await current_app.bus.handle(
            GetUserMessage(
                id=uid
            )
        )
    except InternalException as e:
        abort(make_response(e.errors), 400)

    return result.to_json()


@api.route('/user/<uuid:uid>', methods=['DELETE'])
async def delete_user(uid):
    try:
        result = await current_app.bus.handle(
            DeleteUserMessage(
                id=uid
            )
        )
    except InternalException as e:
        abort(make_response(e.errors), 400)

    return result.to_json()
