from pydantic import BaseModel
from typing import List

class MonitoringQuotesSchema(BaseModel):
    client_id: str 
    api_key: str
    quotes: List[str] = []
