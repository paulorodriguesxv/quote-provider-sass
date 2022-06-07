from dataclasses import dataclass
from http import HTTPStatus
from fastapi import HTTPException, APIRouter, Depends, Response
from typing import List
from quotes.business_rules.exceptions.client_terminal_exceptions import EClientTerminalAlreadyExists

from quotes.business_rules.use_cases.client_terminal_use_case import ClientTerminalUseCase
from quotes.entities.client_terminal.schema import ClientTerminalCreateSchema, ClientTerminalSchema
from quotes.adapters.endpoints.rest_fastapi.fastapi_injector import Injected, get_userid_from_token

router = APIRouter()

@router.get("/",
    summary="Get all client terminals registered from the system",
    description="Return clients terminals",
    response_model=List[ClientTerminalSchema])
async def get_clients(client_terminal_use_case: ClientTerminalUseCase = Injected(ClientTerminalUseCase)):
    client = await client_terminal_use_case.get_all_clients()    
    return client


@router.post("/",
    summary="Register a new client terminal",
    description="Use this endpoint when you want to register a new client terminal",  
    response_model=ClientTerminalSchema,
    status_code=HTTPStatus.CREATED)
async def register_client(client: ClientTerminalCreateSchema, client_terminal_use_case: ClientTerminalUseCase = Injected(ClientTerminalUseCase)):
    try:
        client_c = await client_terminal_use_case.register_client(client)
    except EClientTerminalAlreadyExists:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Clien terminal already registered")
    
    return client_c

@router.delete("/{client_id}", 
    summary="Remove a terminal",
    description="Use this endpoint when you want to remove a terminal.",   
    status_code=204,
    responses={
        204: {"description": "User created", "content": None},
        404: {"description": "When user not found"},
        418: {"description": "Missing Authorization header"}})
async def users(
    client_id: str, 
    client_terminal_use_case: ClientTerminalUseCase = Injected(ClientTerminalUseCase)):

    await client_terminal_use_case.remove_client_terminal(client_id)

    return Response(status_code=HTTPStatus.NO_CONTENT)