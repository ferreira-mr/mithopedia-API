from pydantic import BaseModel, validator
from datetime import datetime
from typing import List, Optional
# from schemas.users import  UserRead
class CommentCreate(BaseModel):
    id_user: int
    comment: str
    date: datetime
    last_update: datetime
    likes: int
    status: int
    god_id: Optional[int] = None
    mytology_id: Optional[int] = None
    history_id: Optional[int] = None

    @validator('status')
    def validate_status(cls, value):
        if value not in [1, 2]:
            raise ValueError("Status must be either 1 or 2")
        return value


class CommentRead(BaseModel):
    id: int
    comment: str
    date: datetime
    last_update: datetime
    likes: int
    status: int
    god_id: Optional[int] = None
    user: dict
    mytology_id: Optional[int] = None
    history_id: Optional[int] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            id_user=obj.id_user.id,  # Acessando o ID do usuário corretamente
            comment=obj.comment,
            date=obj.date,
            last_update=obj.last_update,
            likes=obj.likes,
            status=obj.status,
            god_id=obj.god.id if obj.god else None,  # Garantindo que seja um ID
            mytology_id=obj.mytology.id if obj.mytology else None,
            history_id=obj.history.id if obj.history else None,
        )


class CommentUpdate(BaseModel):
    id_user: Optional[int] = None
    comment: Optional[str] = None
    date: Optional[datetime] = None
    last_update: Optional[datetime] = None
    likes: Optional[int] = None
    status: Optional[int] = None
    god_id: Optional[int] = None
    mytology_id: Optional[int] = None
    history_id: Optional[int] = None

    @validator('status', always=True)
    def validate_status(cls, value):
        if value not in [1, 2]:
            raise ValueError("Status must be either 1 or 2")
        return value


class CommentReadList(BaseModel):
    comments: List[CommentRead]

    class Config:
        from_attributes = True  # Permite compatibilidade com ORM
