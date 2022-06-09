from typing import List
from pydantic import BaseModel

from quotes.entities.crud_repository import ICrudRepository
from quotes.adapters.gateway.sql_alchemy.database import SessionDatabase, SqlAlchemyBase
from quotes.adapters.gateway.sql_alchemy.repository.exceptions import ERegisterNotExists
from sqlalchemy.orm import Session

class ReadWriteRepository(ICrudRepository):
    def __init__(self, 
        session: SessionDatabase,
        sql_alchemy_model: SqlAlchemyBase,
        schema: BaseModel) -> None:
        self.sql_alchemy_model = sql_alchemy_model
        self.schema = schema
        self.session = session

    def get_all(self) -> List[BaseModel]:
        with self.session.scope() as session:
            data = session.query(self.sql_alchemy_model).all()
            return list(map(self.schema.from_orm, data))

    def get_by_id(self, id: str) -> BaseModel:
        with self.session.scope() as session:
            return session.query(self.sql_alchemy_model).filter(self.sql_alchemy_model.id==id).first()

    def add(self, model: BaseModel) -> BaseModel:
        with self.session.scope() as session:
            db_data = self.sql_alchemy_model(**model.dict())    
            session.add(db_data)
            session.commit()
            
            #session.refresh(db_data)
            db_data = session.query(self.sql_alchemy_model).filter(self.sql_alchemy_model.id==model.id).first()
            return self.schema.from_orm(db_data)

    def delete(self, id: str):        
        with self.session.scope() as session:
            item = session.query(self.sql_alchemy_model).filter(self.sql_alchemy_model.id==id)
            data = item.first()
            item.delete()
            session.commit()

            return data



    def update(self, id: str, updated_model: BaseModel):        
        with self.session.scope() as session:
            stored_data = session.query(self.sql_alchemy_model).filter(self.sql_alchemy_model.id==id).first()
            if not stored_data: 
                raise ERegisterNotExists()
                        
            for prop in stored_data.__mapper__.attrs.keys():
                new_value = getattr(updated_model, prop)
                if type(new_value) not in [bool]:
                    new_value = str(getattr(updated_model, prop))
                if new_value:
                    setattr(stored_data, prop, new_value)

            session.commit()

            return self.schema.from_orm(stored_data)
