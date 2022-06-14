from abc import abstractmethod

from pydantic import BaseModel
from quotes.entities.crud_repository import ICrudRepository


class IClientTerminalRepository(ICrudRepository):
           
    @abstractmethod
    async def get_by_id_and_api_key(self, id: str, api_key: str) -> BaseModel:
        pass
    