import logging
from injector import inject
from dataclasses import dataclass
from datetime import datetime
from quotes.adapters.gateway.redis.pool import get_redis_pool
from quotes.business_rules.exceptions.client_terminal_exceptions import EClientTerminalAlreadyExists, EClientTerminalDoesNotExists
from quotes.business_rules.use_cases.client_terminal_use_case import ClientTerminalUseCase
from quotes.entities.client_terminal.repository import IClientTerminalRepository
from quotes.entities.client_terminal.schema import ClientTerminalCreateSchema, ClientTerminalSchema
from quotes.entities.quotes.schema import MonitoringQuotesSchema

logger = logging.getLogger(__name__)

CONNECTED_CLIENTS_KEY = "CONNECTED_CLIENTS"
QUOTE_MONITORING_KEY = "QUOTE_MONITORING"

@inject
@dataclass
class QuotesUseCase():
    client_terminal_use: ClientTerminalUseCase

    async def _validate_client_terminal(self, client_id: str, client_api_key: str):
        client = await self.client_terminal_use.get_client_by_api_key(
            client_id, client_api_key)
        
        if not client:
            raise EClientTerminalDoesNotExists()
        
        return True
            
    async def validate_client_terminal(self, client_id: str, client_api_key: str):
        return await self._validate_client_terminal(client_id, client_api_key)
    
    async def get_connect_clients():

        pool = await get_redis_pool()

        clients = await pool.hgetall(CONNECTED_CLIENTS_KEY)
        return clients
    
    async def update_connected_client(self, client_id: str, connected: bool):
        pool = await get_redis_pool()
        
        if connected:
            await pool.hset(CONNECTED_CLIENTS_KEY, client_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            await pool.hdel(CONNECTED_CLIENTS_KEY, client_id)                    

        logger.debug(
            f"Client updated on redis: {client_id}")
        
    async def set_quote_monitoring(self, quotes_to_monitoring: MonitoringQuotesSchema):        
        await self._validate_client_terminal(quotes_to_monitoring.client_id, quotes_to_monitoring.api_key)
                
        pool = await get_redis_pool()                   
         
        await pool.hset(QUOTE_MONITORING_KEY, quotes_to_monitoring.client_id, ';'.join(quotes_to_monitoring.quotes))
        
    async def get_quote_monitoring(self, client_id: str):        
        pool = await get_redis_pool()                   
        
        all_quotes = await pool.hgetall(QUOTE_MONITORING_KEY) 
        quotes = all_quotes.get(client_id)
        return [quote for quote in quotes.split(';')] if quotes else []
        