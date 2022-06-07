from sqlalchemy import Column, String, DateTime
from quotes.adapters.gateway.sql_alchemy.database import SqlAlchemyBase


class ClientTerminal(SqlAlchemyBase):
    __tablename__ = "client_terminals"

    id = Column(String(255), primary_key=True, unique=True, index=True)
    client_name = Column(String(14), unique=True, index=True, nullable=False)
    api_key = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)    
