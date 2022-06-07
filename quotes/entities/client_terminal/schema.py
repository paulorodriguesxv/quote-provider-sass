from uuid import uuid4
from pydantic import BaseModel, Field, constr
from typing import Optional, List
from datetime import datetime

def get_uuid():
    return uuid4().hex


class ClientTerminalSchema(BaseModel):
    id: str = Field(default_factory=get_uuid)
    client_name: str
    api_key: constr(max_length=14, regex='^[a-zA-Z0-9]+$') = ...
    created_at: datetime = ...

    class Config:
        orm_mode = True

class ClientTerminalCreateSchema(BaseModel):
    client_name: str