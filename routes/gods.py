from typing import Annotated
from fastapi import FastAPI, APIRouter, HTTPException, File, UploadFile
import shutil
import os
from schemas.comments import CommentRead
from models.gods import GodsDB
from schemas.gods import GodsCreate, GodsRead, GodsUpdate, GodsReadList

app = FastAPI()
router = APIRouter(prefix="/gods", tags=["GODS"])

UPLOAD_DIRECTORY = "uploads"

# Criar diretório de upload se não existir
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@router.post("/files/")
async def create_file(fileb: Annotated[UploadFile, File()]):
    file_location = os.path.join(UPLOAD_DIRECTORY, fileb.filename)
    with open(file_location, "wb") as file:
        shutil.copyfileobj(fileb.file, file)
    return {"file_location": file_location}


@router.post('', response_model=GodsRead)
def create_gods(new_god: GodsCreate):
    god = GodsDB.create(**new_god.dict())
    return GodsRead.from_orm(god)


@router.put('/{gods_id}', response_model=GodsRead)
def update_gods(gods_id: int, updated_god: GodsUpdate):
    god = GodsDB.get_or_none(GodsDB.id == gods_id)
    if not god:
        raise HTTPException(status_code=404, detail="God not found")

    # Atualiza campos usando um loop
    for field, value in updated_god.dict().items():
        setattr(god, field, value)

    god.save()
    return GodsRead.from_orm(god)


@router.get('', response_model=GodsReadList)
def list_gods():
    gods = GodsDB.select()
    gods_list = []

    for god in gods:
        comments = god.comments
        comments_list = [CommentRead.from_orm(comment) for comment in comments]

        god_read = GodsRead.from_orm(god)
        god_read.comments = comments_list
        gods_list.append(god_read)

    return {'gods': gods_list}


@router.get('/{god_id}', response_model=GodsRead)
def read_gods(god_id: int):
    god = GodsDB.get_or_none(GodsDB.id == god_id)
    if not god:
        raise HTTPException(status_code=404, detail="God not found")
    return GodsRead.from_orm(god)


@router.delete('/{god_id}', response_model=GodsRead)
def delete_god(god_id: int):
    god = GodsDB.get_or_none(GodsDB.id == god_id)
    if not god:
        raise HTTPException(status_code=404, detail="God not found")
    god.delete_instance()
    return GodsRead.from_orm(god)


app.include_router(router)
