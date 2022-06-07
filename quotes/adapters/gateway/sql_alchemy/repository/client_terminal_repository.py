from injector import inject 
from dataclasses import dataclass
from typing import List
from quotes.adapters.gateway.sql_alchemy.database import SessionDatabase

from quotes.adapters.gateway.sql_alchemy.models.client_terminal import ClientTerminal
from quotes.adapters.gateway.sql_alchemy.repository.readwrite_repository import ReadWriteRepository
from quotes.entities.client_terminal.repository import IClientTerminalRepository
from quotes.entities.client_terminal.schema import ClientTerminalSchema

@inject
class ClientTerminalRepository(ReadWriteRepository, IClientTerminalRepository):
    
    def __init__(self, 
        session: SessionDatabase) -> None:
        super(ClientTerminalRepository, self).__init__(session, ClientTerminal, ClientTerminalSchema)
        self.session = session
