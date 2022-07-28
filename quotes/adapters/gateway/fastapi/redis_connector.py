import asyncio
from asyncio.log import logger
import aioredis
from fastapi import WebSocket, WebSocketDisconnect

from quotes.adapters.gateway.redis.pool import get_redis_pool


async def redis_connector(
    websocket: WebSocket, redis_pool: aioredis.RedisPool
):    
    async def consumer_handler(ws: WebSocket, r):
        try:
            while True:
                message = await ws.receive_text()
                if message:
                    await r.publish("chat:c", message)
        except WebSocketDisconnect as exc:
            # TODO this needs handling better
            logger.error(exc)
            
    consumer_task = consumer_handler(websocket, redis_pool)
    
    done, pending = await asyncio.wait(
        [consumer_task], return_when=asyncio.FIRST_COMPLETED,
    )
    logger.debug(f"Done task: {done}")
    for task in pending:
        logger.debug(f"Canceling task: {task}")
        task.cancel()
    redis_pool.close()
    await redis_pool.wait_closed()    