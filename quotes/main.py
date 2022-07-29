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
from fastapi_plugins import depends_redis, redis_plugin
import fastapi_plugins
from decouple import config

DefaultConfig.init_logging()

app = rest_fastapi.build(injector=fastapi_beans)
app = fastapi_plugins.register_middleware(app)


REDIS_HOST = config("REDIS_HOST", default="localhost")
REDIS_PORT = config("REDIS_PORT", default="6379")
REDIS_PASSWORD = config("REDIS_PASSWORD", default="Redis2019!")
            
class AppSettings(fastapi_plugins.RedisSettings):
    api_name: str = str(__name__)
    redis_url: str = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}'

config = AppSettings()

@app.on_event("startup")
async def startup_event():
    await fastapi_plugins.config_plugin.init_app(app, config)
    await fastapi_plugins.config_plugin.init()
    await redis_plugin.init_app(app, config=config)
    await redis_plugin.init()
    #execute_migration()

@app.on_event("shutdown")
async def on_shutdown() -> None:
    await redis_plugin.terminate()