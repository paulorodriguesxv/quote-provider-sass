import json
import logging
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketState

LOGGING_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT)


app = FastAPI()

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


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def check_authorized_key(self, data: str, websocket: WebSocket):
        authorized_keys = ["hJKLAshgdkjlashdklJsdjasd"]

        api_key = data.get("api_key")
        if not api_key in authorized_keys:
            logging.error(f"Client not authorized")
            self.disconnect(websocket)
            return

        websocket.api_key = api_key
        logging.info(f"Client authorized ")
            
    async def handle_command(self, payload, websocket: WebSocket):
        if not "command" in payload:
            return

        if "AUTHORIZATION" in payload["command"]:
            await self.check_authorized_key(payload["data"], websocket)
            return

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        websocket.api_key = None

    def disconnect(self, websocket: WebSocket):        
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        print(self.active_connections)
        for connection in self.active_connections:            

            if not connection.api_key:
                return

            try:
                await connection.send_text(message)
            except Exception as err:
                print(connection.client_state)
                self.disconnect(connection)


manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:      
            data = await websocket.receive()
            data = data.get('text', data.get('bytes'))
            if type(data) == bytes:
                data = data.decode("utf-8")

            print(data)      

            payload_decoded = json.loads(data)
            await manager.handle_command(payload_decoded, websocket)
            await manager.broadcast(data)

    except WebSocketDisconnect as error:
        print(error)
        manager.disconnect(websocket)
        #await manager.broadcast(f"Client #{client_id} left the chat")
