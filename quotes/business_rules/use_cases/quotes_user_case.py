import logging
from injector import inject
from dataclasses import dataclass
from datetime import datetime
from quotes.adapters.gateway.redis.pool import get_redis_pool
from quotes.business_rules.exceptions.client_terminal_exceptions import EClientTerminalAlreadyExists, EClientTerminalDoesNotExists
from quotes.business_rules.use_cases.client_terminal_use_case import ClientTerminalUseCase
from quotes.entities.client_terminal.repository import IClientTerminalRepository
from quotes.entities.client_terminal.schema import ClientTerminalCreateSchema, ClientTerminalSchema

logger = logging.getLogger(__name__)

CONNECTED_CLIENTS_KEY = "CONNECTED_CLIENTS"

@inject
@dataclass
class QuotesUseCase():
    client_terminal_use: ClientTerminalUseCase

    async def validate_client_terminal(self, id: str, client_api_key: str):
        client = await self.client_terminal_use.get_client_by_api_key(id, client_api_key)
        if not client:
            raise EClientTerminalDoesNotExists()

        return True
    
    
    async def get_connect_clients():

        pool = await get_redis_pool()

        clients = await pool.hgetall(CONNECTED_CLIENTS_KEY, encoding='utf-8')
        return clients
    
    async def update_connected_client(self, client_id: str, connected: bool):

        pool = await get_redis_pool()

        #clients = await pool.hgetall(CONNECTED_CLIENTS_KEY, encoding='utf-8')
        
        if connected:
            await pool.hset(CONNECTED_CLIENTS_KEY, client_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            await pool.hdel(CONNECTED_CLIENTS_KEY, client_id)                    

        logger.debug(
            f"Client updated on redis: {client_id}")