from redis import asyncio as aioredis
import asyncio
import os
from aiohttp_session.redis_storage import RedisStorage


def redis_connect(app):
    async def make_redis_pool():
        redis_password = os.getenv('REDIS_PASSWORD')
        if redis_password:
            redis_address = 'redis://:{}@{}:{}'.format(redis_password, os.getenv('REDIS_HOST', 'redis'), os.getenv('REDIS_PORT', '6379'))
        else:
            redis_address = 'redis://{}:{}'.format(os.getenv('REDIS_HOST', 'redis'), os.getenv('REDIS_PORT', '6379'))
        return await aioredis.from_url(redis_address)

    loop = asyncio.get_event_loop()
    redis_pool = loop.run_until_complete(make_redis_pool())
    storage = RedisStorage(redis_pool)
    return storage, redis_pool
