from fastapi import APIRouter, HTTPException, File, UploadFile
from typing import Annotated
import shutil
import os

from schemas.mytology_history import MytologyReadShort
from models.mytology import MytologyDB
from schemas.gods import GodsRead
from models.history import HistoryDB
from models.gods import GodsDB
from schemas.comments import CommentRead
from models.comments import CommentsDB
from schemas.mytology_history import (
    HistoryCreate,
    HistoryRead,
    HistoryUpdate,
    HistoryReadList
)

router = APIRouter(prefix="/history", tags=["STORIES"])

UPLOAD_DIRECTORY = "uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


@router.post("/files/", response_model=HistoryRead)
async def create_file(fileb: Annotated[UploadFile, File()]):
    file_location = f"{UPLOAD_DIRECTORY}/{fileb.filename}"
    with open(file_location, "wb") as file:
        shutil.copyfileobj(fileb.file, file)
    return {"file_location": file_location}


@router.post('', response_model=HistoryRead)
def create_history(new_history: HistoryCreate):
    god = GodsDB.get_or_none(GodsDB.id == new_history.god_id)
    mythology = MytologyDB.get_or_none(MytologyDB.id == new_history.mythology_id)

    if not god:
        raise HTTPException(status_code=404, detail="God not found")
    if not mythology:
        raise HTTPException(status_code=404, detail="Mythology not found")

    history = HistoryDB.create(
        title=new_history.title,
        content=new_history.content,
        author=new_history.author,
        source=new_history.source,
        publish_time=new_history.publish_time,
        last_updated=new_history.last_updated,
        views=new_history.views,
        age_classification=new_history.age_classification,
        mythology=mythology,
        god=god
    )

    return HistoryRead.from_orm(history)


@router.put('/{story_id}', response_model=HistoryRead)
def update_history(story_id: int, updated_history: HistoryUpdate):
    history = HistoryDB.get_or_none(HistoryDB.id == story_id)
    if not history:
        raise HTTPException(status_code=404, detail="History not found")

    for field, value in updated_history.dict(exclude_unset=True).items():
        setattr(history, field, value)

    history.save()
    return HistoryRead.from_orm(history)


@router.get('/stories', response_model=HistoryReadList)
def list_stories():
    stories = HistoryDB.select()  # Recupera todas as histórias
    # story_list = [HistoryRead.from_orm(story) for story in stories]
    return {'stories': stories}  # Retorna a lista de histórias


@router.get('/{story_id}', response_model=HistoryRead)
def read_history(story_id: int):
    history = HistoryDB.get_or_none(HistoryDB.id == story_id)
    if not history:
        raise HTTPException(status_code=404, detail="History not found")

    # Converter os dados para Pydantic
    god_data = GodsRead.from_orm(history.god)
    mythology_data = MytologyReadShort.from_orm(history.mythology)

    # Recuperando e convertendo os comentários
    comments = CommentsDB.select().where(CommentsDB.history == history)
    comments_list = [CommentRead.from_orm(comment) for comment in comments]

    return HistoryRead(
        title=history.title,
        content=history.content,
        author=history.author,
        source=history.source,
        publish_time=history.publish_time,
        last_updated=history.last_updated,
        views=history.views,
        age_classification=history.age_classification,
        god_id=god_data.id,
        mythology=mythology_data,
        comments=comments_list  # Incluindo os comentários na resposta
    )




@router.delete('/{story_id}', response_model=HistoryRead)
def delete_history(story_id: int):
    history = HistoryDB.get_or_none(HistoryDB.id == story_id)
    if not history:
        raise HTTPException(status_code=404, detail="History not found")

    history.delete_instance()
    return HistoryRead.from_orm(history)


@router.get('/gods/{god_id}', response_model=HistoryReadList)
def read_history_by_god(god_id: int):
    god = GodsDB.get_or_none(GodsDB.id == god_id)
    if not god:
        raise HTTPException(status_code=404, detail="God not found")

    stories = HistoryDB.select().where(HistoryDB.god == god)
    return {'stories': [HistoryRead.from_orm(story) for story in stories]}


@router.post('/gods/history')
def add_god_to_history(god_id: int, history_id: int):
    history = HistoryDB.get_or_none(HistoryDB.id == history_id)
    god = GodsDB.get_or_none(GodsDB.id == god_id)

    if not history or not god:
        raise HTTPException(status_code=404, detail="History or God not found")

    # Assuming a Many-to-Many relationship, implement the linking here
    # HistoryGods.create(history=history, god=god)

    return {'status': 'ok'}
