from http import HTTPStatus
from injector import Injector
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from quotes.adapters.endpoints.rest_fastapi.fastapi_injector import attach_injector
from quotes.adapters.endpoints.rest_fastapi.controllers import client_terminal_controller
from quotes.adapters.endpoints.rest_fastapi.controllers import quote_controller


def build(injector: Injector):
    app = FastAPI(
        redoc_url="/",
        title="Quotes Provider API",
        description="Quotes is realtime provider for stock quotes",
        version="0.1.0",
        terms_of_service="https://github.com/paulorodriguesxv/",
        contact={
            "name": "Paulo Rodrigues",
            "url": "https://github.com/paulorodriguesxv/",
        },
        license_info={
            "name": "MIT",
            "url": "https://en.wikipedia.org/wiki/MIT_License",
        },
    )

    app.include_router(client_terminal_controller.router,
                        prefix='/client-terminal',
                        tags=['client-terminal'])

    app.include_router(quote_controller.router,
                        prefix='/quotes',
                        tags=['quotes'])                        


    attach_injector(app, injector)
    
    return app