import aioredis
from decouple import config
import asyncio
import async_timeout
from aioredis.client import PubSub, Redis

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
    
    

STOPWORD = "STOP"


async def reader(channel: aioredis.client.PubSub):
    while True:
        try:
            async with async_timeout.timeout(1):
                message = await channel.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    print(f"(Reader) Message Received: {message}")                    
                await asyncio.sleep(0.01)
        except asyncio.TimeoutError:
            pass


async def main():
    redis = await get_redis_pool()
    pubsub = redis.pubsub()
    await pubsub.subscribe("PETR4")

    future = asyncio.create_task(reader(pubsub))

    await future


if __name__ == "__main__":
    asyncio.run(main())