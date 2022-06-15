import logging
from xmlrpc.client import DateTime
from injector import inject
from dataclasses import dataclass
from datetime import datetime
from quotes.business_rules.exceptions.client_terminal_exceptions import EClientTerminalAlreadyExists, EClientTerminalDoesNotExists
from quotes.entities.client_terminal.repository import IClientTerminalRepository
from quotes.entities.client_terminal.schema import ClientTerminalCreateSchema, ClientTerminalSchema

@inject
@dataclass
class ClientTerminalUseCase():
    client_terminal_repository: IClientTerminalRepository

    async def register_client(self, client: ClientTerminalCreateSchema):
        client_found = self.client_terminal_repository.get_by_id(client.client_name)
        if client_found:
            raise EClientTerminalAlreadyExists()

        client_terminal = ClientTerminalSchema(
            client_name=client.client_name,
            created_at = datetime.now()            
        )        
        data = self.client_terminal_repository.add(client_terminal)

        return data
    
    async def get_client_by_id(self, client_id: str):        
        data = self.client_terminal_repository.get_by_id(client_id)
        return data

    async def get_all_clients(self):
        data = self.client_terminal_repository.get_all()
        return data
 
    async def remove_client_terminal(self, client_id: str):
        return self.client_terminal_repository.delete(client_id)
    
    async def get_client_by_api_key(self, client_id: str, client_api_key: str):
        data = await self.client_terminal_repository.get_by_id_and_api_key(client_id, client_api_key)
        return data
