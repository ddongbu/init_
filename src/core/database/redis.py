import datetime
from typing import Union

from pydantic import BaseModel
from redis import Redis

redis_token: Redis
redis_code: Redis


class RedisData(BaseModel):
    db: str
    key: Union[str, bytes]
    value: Union[str, bytes]
    ttl: Union[int | datetime.timedelta | None]


async def set_data(redis_client: Redis, data: RedisData, is_transaction: bool = False) -> None:
    pipe = redis_client.pipeline(transaction=is_transaction)
    await pipe.set(data.key, data.value)
    if data.ttl:
        await pipe.expire(data.key, data.ttl)
    await pipe.execute()
    pipe.close()


async def get_data(redis_client: Redis, key: str):
    return await redis_client.get(key)


async def delete_data(redis_client: Redis, key: str):
    return await redis_client.delete(key)
