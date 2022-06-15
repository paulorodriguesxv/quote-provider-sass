from dataclasses import dataclass
from http import HTTPStatus
import json
import logging
from typing import List
from fastapi import APIRouter, Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from injector import Inject, Injector, inject, singleton, provider
from starlette.websockets import WebSocketState
from quotes.adapters.endpoints.rest_fastapi.fast_api_beans import fastapi_beans
from quotes.adapters.endpoints.rest_fastapi.controllers.ConnectionManager import ConnectionManager
from quotes.adapters.endpoints.rest_fastapi.fastapi_injector import Injected

from quotes.business_rules.use_cases.client_terminal_use_case import ClientTerminalUseCase
from quotes.business_rules.use_cases.quotes_user_case import QuotesUseCase
from quotes.entities.quotes.schema import MonitoringQuotesSchema

LOGGING_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT)


router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
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


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str,    
    ):
    
    manager: ConnectionManager = fastapi_beans.get(ConnectionManager)
            
    await manager.connect(websocket)
    try:
        while True:      
            data = await websocket.receive()
            data = data.get('text', data.get('bytes'))
            if type(data) == bytes:
                data = data.decode("utf-8")
            payload_decoded = ""
            if data:
                payload_decoded = json.loads(data)
            await manager.handle_command(
                payload_decoded, websocket, client_id)
            await manager.broadcast(data)

    except WebSocketDisconnect as error:
        print(error)
        manager.disconnect(websocket)
        #await manager.broadcast(f"Client #{client_id} left the chat")


@router.post("/monitoring",
    summary="Set quotes to monitoring",    
    description="Use this endpoint when you want to set up quotes to client terminal monitoring",  
    status_code=HTTPStatus.CREATED)
async def set_quotes_to_monitoring(
    quotes: MonitoringQuotesSchema,
    client_terminal_use_case: QuotesUseCase = Injected(QuotesUseCase)):
    await client_terminal_use_case.set_quote_monitoring(quotes)
    
@router.get("/monitoring/{client_id}",	
    summary="Get monitoring quotes",    
    description="Use this endpoint when you want to get quotes monitored by a client terminal",  
    status_code=HTTPStatus.OK)
async def set_quotes_to_monitoring(
    client_id :str,
    client_terminal_use_case: QuotesUseCase = Injected(QuotesUseCase)):
    return await client_terminal_use_case.get_quote_monitoring(client_id)
