from datetime import datetime
from typing import List

from pydantic import BaseModel
from schemas.gods import GodsRead
from schemas.comments import CommentRead

# Classes relacionadas à Mitologia (Mytology)

class MytologyCreate(BaseModel):
    name: str
    sub_description: str
    description: str
    origin: str
    period: str
    gods_qty: int
    sacred_texts: str
    main_mytology: str
    creator: str
    data_creation: datetime
    last_update: datetime
    main_symbol: str  # Path or URL to the image
    mytology_banner: str  # Path or URL to the image
    mytology_profile_img: str  # Path or URL to the image


# Classes relacionadas à História (History)
class HistoryCreate(BaseModel):
    mythology_id: int  # This should be passed when creating a history
    title: str
    content: str
    author: str
    source: str
    publish_time: datetime
    last_updated: datetime
    views: int
    age_classification: int
    god_id: int  # Assuming you still need this


class MytologyReadShort(BaseModel):
    id: int
    name: str  # ou qualquer outro campo relevante

    class Config:
        from_attributes = True


class HistoryRead(BaseModel):
    title: str
    content: str
    author: str
    source: str
    publish_time: datetime
    last_updated: datetime
    views: int
    age_classification: int
    god_id: int
    mythology: MytologyReadShort  # Estrutura correta
    # comments: List[CommentRead] = []  # Incluindo a lista de comentários

    class Config:
        from_attributes = True


class HistoryUpdate(BaseModel):
    mythology_id: int
    title: str
    content: str
    author: str
    source: str
    publish_time: datetime
    last_updated: datetime
    views: int
    age_classification: int
    god: GodsRead  # Usar string para evitar referência circular


class HistoryReadList(BaseModel):
    stories: List[HistoryRead]


class MytologyRead(BaseModel):
    id: int
    name: str
    sub_description: str
    description: str
    origin: str
    period: str
    gods_qty: int
    sacred_texts: str
    main_mytology: str
    creator: str
    data_creation: datetime
    last_update: datetime
    main_symbol: str  # Path or URL to the image
    mytology_banner: str  # Path or URL to the image
    mytology_profile_img: str  # Path or URL to the image
    comments: List[CommentRead] = []  # Lista de comentários
    stories: List[HistoryRead] = []  # Lista de histórias

    class Config:
        from_attributes = True  # Enable ORM compatibility


class MytologyUpdate(BaseModel):
    name: str
    sub_description: str
    description: str
    origin: str
    period: str
    gods_qty: int
    sacred_texts: str
    main_mytology: str
    creator: str
    data_creation: datetime
    last_update: datetime
    main_symbol: str  # Path or URL to the image
    mytology_banner: str  # Path or URL to the image
    mytology_profile_img: str  # Path or URL to the image


class MytologyReadList(BaseModel):
    mytologies: List[MytologyRead]


class MytologyReadListWithHistory(BaseModel):
    name: str
    sub_description: str
    description: str
    origin: str
    period: str
    gods_qty: int
    sacred_texts: str
    main_mytology: str
    creator: str
    data_creation: datetime
    last_update: datetime
    main_symbol: str  # Path or URL to the image
    mytology_banner: str  # Path or URL to the image
    mytology_profile_img: str  # Path or URL to the image
    stories: List[HistoryRead]  # Referência à classe HistoryRead
