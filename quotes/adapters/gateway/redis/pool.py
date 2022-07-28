import aioredis
from decouple import config

REDIS_HOST = config("REDIS_HOST", default="localhost")
REDIS_PORT = config("REDIS_PORT", default="6379")
REDIS_PASSWORD = config("REDIS_PASSWORD", default="Redis2019!")

async def get_redis_pool():
    try:
        pool = aioredis.from_url(
            f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}',
            encoding="utf-8",
            decode_responses=True,
            db=0)
        return pool
    except ConnectionRefusedError as e:
        print('cannot connect to redis on:', REDIS_HOST, REDIS_PORT)
        return None
    