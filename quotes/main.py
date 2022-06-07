from injector import Injector
from sqlalchemy.orm import Session
from migrations.migration_helper import execute_migration


from quotes.adapters.gateway.sql_alchemy.database import SessionDatabase
from quotes.adapters.gateway.sql_alchemy.repository.client_terminal_repository import ClientTerminalRepository
from quotes.business_rules.use_cases.client_terminal_use_case import  ClientTerminalUseCase


# for fast api
from quotes.adapters.endpoints import rest_fastapi
from quotes.entities.client_terminal.repository import IClientTerminalRepository

def configure(binder):
    # database
    binder.bind(SessionDatabase, to=SessionDatabase)

    # repositories
    binder.bind(IClientTerminalRepository, to=ClientTerminalRepository)
    
    #use cases
    binder.bind(ClientTerminalUseCase, to=ClientTerminalUseCase)

injector = Injector([configure])
app = rest_fastapi.build(injector=injector)


@app.on_event("startup")
async def startup_event():
    execute_migration()
