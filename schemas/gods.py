from pydantic import BaseModel
from datetime import datetime
from typing import List
from schemas.comments import CommentRead

class GodsCreate(BaseModel):
    name: str
    sub_description: str
    description: str
    symbol: str
    domain: str
    kinship: str
    caracteristics: str
    sacred_animal: str
    sacred_colour: str
    data_creation: datetime
    last_update: datetime

    class Config:
        from_attributes = True


class GodsRead(BaseModel):
    id: int
    name: str
    sub_description: str
    description: str
    symbol: str
    domain: str
    kinship: str
    caracteristics: str
    sacred_animal: str
    sacred_colour: str
    data_creation: datetime
    last_update: datetime
    comments: List[CommentRead] = []

    class Config:
        from_attributes = True  # Permite compatibilidade com ORM

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            name=obj.name,
            sub_description=obj.sub_description,
            description=obj.description,
            symbol=obj.symbol,
            domain=obj.domain,
            kinship=obj.kinship,
            caracteristics=obj.caracteristics,
            sacred_animal=obj.sacred_animal,
            sacred_colour=obj.sacred_colour,
            data_creation=obj.data_creation,
            last_update=obj.last_update,
            comments=[CommentRead.from_orm(comment) for comment in obj.comments]  # Converte comentários corretamente
        )


class GodsUpdate(BaseModel):
    name: str
    sub_description: str
    description: str
    symbol: str
    domain: str
    kinship: str
    caracteristics: str
    sacred_animal: str
    sacred_colour: str
    data_creation: datetime
    last_update: datetime

    class Config:
        from_attributes = True


class GodsReadList(BaseModel):
    gods: list[GodsRead]

    class Config:
        from_attributes = True
