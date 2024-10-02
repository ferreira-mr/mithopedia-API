# from pydantic import BaseModel
# from datetime import datetime
# from gods import GodsRead
#
# class HistoryCreate(BaseModel):
#     mythology_id: int  # This should be passed when creating a history
#     title: str
#     content: str
#     author: str
#     source: str
#     publish_time: datetime
#     last_updated: datetime
#     views: int
#     age_classification: int
#     god_id: int  # Assuming you still need this
#
#
# class HistoryRead(BaseModel):
#     # Mover o import para dentro do método, para evitar importação circular
#     mythology_id: int
#     title: str
#     content: str
#     author: str
#     source: str
#     publish_time: datetime
#     last_updated: datetime
#     views: int
#     age_classification: int
#     god: GodsRead  # Usar string para evitar referência circular
#     mythology: MytologyRead
#
#     class Config:
#         from_attributes = True  # Enable ORM compatibility
#
#     @staticmethod
#     def imports():
#         # Importar aqui para evitar circularidade
#         from schemas.mytology_history import MytologyRead
#         from schemas.gods import GodsRead
#
#
# class HistoryUpdate(BaseModel):
#     mythology_id: int
#     title: str
#     content: str
#     author: str
#     source: str
#     publish_time: datetime
#     last_updated: datetime
#     views: int
#     age_classification: int
#     god: GodsRead  # Evitar referência circular
#
#
# class HistoryReadList(BaseModel):
#     stories: list[HistoryRead]  # Usar string para evitar circularidade
