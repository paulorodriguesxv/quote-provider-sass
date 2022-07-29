import asyncio
import json
import logging
import aioredis
from aioredis.client import PubSub, Redis
from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect
from quotes.adapters.gateway.redis.pool import get_redis_pool
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/datafeed/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@router.get("/")
async def get():
    return HTMLResponse(html)

@router.websocket('/ws')
async def ws_voting_endpoint(websocket: WebSocket):
    await websocket.accept()
    await redis_connector(websocket)


async def redis_connector(websocket: WebSocket):

    async def consumer_handler(ws: WebSocket, pubsub: PubSub):
        try:
            while True:
                message = await ws.receive_text()
                if not (message and (":" in message)):
                    continue
                message_type, message_content = message.split(":")
                if message_type == '"subscribe"':
                    tickers = json.loads(message_content)
                    for ticker in tickers:
                        await pubsub.subscribe(ticker)
                        
                if message_type == '"unsubscribe"':
                    tickers = json.loads(message_content)
                    for ticker in tickers:
                        await pubsub.unsubscribe(ticker)                        
        except WebSocketDisconnect as exc:
            # TODO this needs handling better
            logger.error(exc)
            
    async def producer_handler(pubsub: PubSub, ws: WebSocket):
        await pubsub.subscribe("PETR4")
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message:
                    await ws.send_text(f"{message['channel']}:{message.get('data')}")
        except Exception as exc:
            # TODO this needs handling better
            logger.error(exc)

    conn = await get_redis_pool()
    pubsub = conn.pubsub()

    consumer_task = consumer_handler(websocket, pubsub)
    producer_task = producer_handler(pubsub=pubsub, ws=websocket)
    
    done, pending = await asyncio.wait(
        [consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED,
    )
    logger.debug(f"Done task: {done}")
    for task in pending:
        logger.debug(f"Canceling task: {task}")
        task.cancel()
