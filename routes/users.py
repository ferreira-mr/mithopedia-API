from fastapi import APIRouter, HTTPException
from models.users import UserDB
from schemas.users import UserCreate, UserRead, UserUpdate, UserReadList

router = APIRouter(prefix="/users", tags=["USERS"])

@router.post('', response_model=UserRead)
def create_user(new_user: UserCreate):
    user = UserDB.create(**new_user.dict())  # Cria o usuário no banco de dados
    return UserRead.from_orm(user)  # Converte para o modelo Pydantic

@router.get('', response_model=UserReadList)
def list_user():
    users = UserDB.select()  # Seleciona todos os usuários
    return {'users': [UserRead.from_orm(user) for user in users]}  # Converte cada usuário

@router.get('/{user_id}', response_model=UserRead)
def read_user(user_id: int):
    user = UserDB.get_or_none(UserDB.id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.from_orm(user)  # Converte para o modelo Pydantic

@router.put('/{user_id}', response_model=UserRead)
def update_user(user_id: int, updated_user: UserUpdate):
    user = UserDB.get_or_none(UserDB.id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = updated_user.name
    user.email = updated_user.email
    user.password = updated_user.password
    user.type = updated_user.type
    user.save()  # Salva as alterações
    return UserRead.from_orm(user)  # Converte para o modelo Pydantic

@router.delete('/{user_id}', response_model=UserRead)
def delete_user(user_id: int):
    user = UserDB.get_or_none(UserDB.id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete_instance()  # Deleta o usuário
    return UserRead.from_orm(user)  # Converte para o modelo Pydantic
