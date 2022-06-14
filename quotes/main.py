from injector import Injector, singleton
from sqlalchemy.orm import Session
from migrations.migration_helper import execute_migration
from quotes.adapters.endpoints.rest_fastapi.fast_api_beans import fastapi_beans

from quotes.adapters.gateway.sql_alchemy.database import SessionDatabase
from quotes.adapters.gateway.sql_alchemy.repository.client_terminal_repository import ClientTerminalRepository
from quotes.business_rules.use_cases.client_terminal_use_case import  ClientTerminalUseCase
from quotes.adapters.endpoints import rest_fastapi
from quotes.business_rules.use_cases.quotes_user_case import QuotesUseCase
from quotes.entities.client_terminal.repository import IClientTerminalRepository
from quotes.infrastructure.config import DefaultConfig
from quotes.adapters.endpoints.rest_fastapi.fast_api_beans import configure
DefaultConfig.init_logging()

app = rest_fastapi.build(injector=fastapi_beans)


@app.on_event("startup")
async def startup_event():
    pass
    #execute_migration()
