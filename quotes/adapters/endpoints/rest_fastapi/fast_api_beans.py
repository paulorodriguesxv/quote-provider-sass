from injector import singleton, Injector
from quotes.adapters.endpoints.rest_fastapi.controllers.connection_manager import ConnectionManager
from quotes.adapters.gateway.sql_alchemy.database import SessionDatabase
from quotes.adapters.gateway.sql_alchemy.repository.client_terminal_repository import ClientTerminalRepository
from quotes.business_rules.use_cases.client_terminal_use_case import ClientTerminalUseCase
from quotes.business_rules.use_cases.quotes_user_case import QuotesUseCase
from quotes.entities.client_terminal.repository import IClientTerminalRepository


def configure(binder):
    # database
    binder.bind(SessionDatabase, to=SessionDatabase)

    # repositories
    binder.bind(IClientTerminalRepository, to=ClientTerminalRepository)
    
    #use cases
    binder.bind(ClientTerminalUseCase, to=ClientTerminalUseCase)
    binder.bind(QuotesUseCase, to=QuotesUseCase)
    binder.bind(ConnectionManager, to=ConnectionManager, scope=singleton)
    
    
fastapi_beans = Injector([configure])       