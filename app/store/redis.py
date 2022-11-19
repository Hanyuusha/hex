import uuid
from uuid import UUID

import aioredis

from app.config.store import get_redis_url

from .adapter import DataBaseAdapter, ModelUser


class RedisAdapter(DataBaseAdapter):

    redis = None

    def __init__(self):
        pool = aioredis.ConnectionPool.from_url(url=get_redis_url(), max_connections=10, decode_responses=True)
        self.redis = aioredis.Redis(connection_pool=pool)

    async def get_user(self, uid: UUID) -> ModelUser | None:
        payload: dict = await self.redis.hgetall(str(uid))

        if payload is None or len(payload.keys()) == 0:
            return None

        return ModelUser(
            id=UUID(payload.get('id')),
            first_name=payload.get('first_name'),
            second_name=payload.get('second_name'),
        )

    async def create_user(self, user: ModelUser) -> UUID:
        uid = uuid.uuid4()
        user.id = uid

        await self.redis.hset(str(uid), mapping=user.to_json())
        return uid

    async def delete_user(self, uid: UUID) -> bool:
        if not await self.redis.exists(str(uid)):
            return False

        await self.redis.delete(str(uid))
        return True

    async def update_user(self, uid: UUID, payload: dict):
        await self.redis.hset(str(uid), mapping=payload)
