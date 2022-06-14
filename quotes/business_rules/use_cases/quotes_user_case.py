from injector import inject
from dataclasses import dataclass
from datetime import datetime
from quotes.business_rules.exceptions.client_terminal_exceptions import EClientTerminalAlreadyExists, EClientTerminalDoesNotExists
from quotes.business_rules.use_cases.client_terminal_use_case import ClientTerminalUseCase
from quotes.entities.client_terminal.repository import IClientTerminalRepository
from quotes.entities.client_terminal.schema import ClientTerminalCreateSchema, ClientTerminalSchema

@inject
@dataclass
class QuotesUseCase():
    client_terminal_use: ClientTerminalUseCase

    async def validate_client_terminal(self, id: str, client_api_key: str):
        client = await self.client_terminal_use.get_client_by_api_key(id, client_api_key)
        if not client:
            raise EClientTerminalDoesNotExists()

        return True