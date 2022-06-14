from dataclasses import dataclass
import logging
from typing import List
from fastapi import WebSocket
from injector import Inject, Injector, inject, singleton, provider
from quotes.business_rules.use_cases.quotes_user_case import QuotesUseCase


@singleton
@inject
class ConnectionManager():
    
    def __init__(self, quotes_use_case: QuotesUseCase) -> None:
        self.quotes_use_case: QuotesUseCase = quotes_use_case
        self.active_connections: List[WebSocket] = []
    
    async def check_authorized_key(self, 
        data: str,
        websocket: WebSocket,
        client_id: str):

        api_key = data.get("api_key")   
        has_api_key = await self.quotes_use_case.validate_client_terminal(client_id, api_key)
        if not has_api_key:
            logging.error(f"Client not authorized")
            self.disconnect(websocket)
            return
        
        websocket.api_key = api_key
        logging.info(f"Client authorized ")
            
    async def handle_command(self, payload, websocket: WebSocket, client_id: str):
        print(payload)
        if not "command" in payload:
            return

        if "AUTHORIZATION" in payload["command"]:
            await self.check_authorized_key(payload["data"], websocket, client_id)
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
        for connection in self.active_connections:            

            if not connection.api_key:
                return

            try:
                await connection.send_text(message)
            except Exception as err:
                print(connection.client_state)
                self.disconnect(connection)
