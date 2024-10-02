from pydantic import BaseModel, field_validator
from schemas.comments import CommentRead
from typing import List

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    type: int

    @field_validator('type')
    def type_of_user(cls, value):
        if value not in [1, 2]:
            raise ValueError("Type must be either 1 or 2")
        return value

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    password: str
    type: int
    comments: List[CommentRead] = []  # Inicializa como uma lista vazia

    class Config:
        from_attributes = True  # Permite o uso de from_orm

class UserUpdate(BaseModel):
    name: str
    email: str
    password: str
    type: int

    @field_validator('type')
    def type_of_user(cls, value):
        if value not in [1, 2]:
            raise ValueError("Type must be either 1 or 2")
        return value

class UserReadList(BaseModel):
    users: List[UserRead]
