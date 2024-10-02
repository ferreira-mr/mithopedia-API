from fastapi import FastAPI, APIRouter, HTTPException, File, UploadFile
from typing import Annotated
import shutil
import os
from models.history import HistoryDB
from models.mytology import MytologyDB
from schemas.mytology_history import (
    MytologyCreate,
    MytologyRead,
    MytologyUpdate,
    MytologyReadList,
    HistoryRead
)
from schemas.comments import CommentRead
from models.comments import CommentsDB

app = FastAPI()
router = APIRouter(prefix="/mythologies", tags=["MYTHOLOGIES"])

UPLOAD_DIRECTORY = "uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post('/files/')
async def create_file(fileb: Annotated[UploadFile, File()]):
    file_location = f"{UPLOAD_DIRECTORY}/{fileb.filename}"
    with open(file_location, "wb") as file:
        shutil.copyfileobj(fileb.file, file)
    return {"file_location": file_location}

@router.post('', response_model=MytologyRead)
def create_mytology(new_mytology: MytologyCreate):
    mytology = MytologyDB.create(**new_mytology.dict())
    return MytologyRead.from_orm(mytology)

@router.put('/{mythology_id}', response_model=MytologyRead)
def update_mytology(mythology_id: int, updated_mytology: MytologyUpdate):
    mytology = MytologyDB.get_or_none(MytologyDB.id == mythology_id)
    if not mytology:
        raise HTTPException(status_code=404, detail="Mythology not found")

    for field, value in updated_mytology.dict(exclude_unset=True).items():
        setattr(mytology, field, value)

    mytology.save()
    return MytologyRead.from_orm(mytology)

@router.get('', response_model=MytologyReadList)
def list_mytology():
    mytologies = MytologyDB.select()
    mytology_list = []

    for mytology in mytologies:
        stories = HistoryDB.select().where(HistoryDB.mytology_id == mytology.id)
        story_list = [HistoryRead.from_orm(history) for history in stories]
        comments = mytology.comments
        comments_list = [CommentRead.from_orm(comment) for comment in comments]

        mytology_read = MytologyRead(
            id=mytology.id,
            name=mytology.name,
            sub_description=mytology.sub_description,
            description=mytology.description,
            origin=mytology.origin,
            period=mytology.period,
            gods_qty=mytology.gods_qty,
            sacred_texts=mytology.sacred_texts,
            main_mytology=mytology.main_mytology,
            creator=mytology.creator,
            data_creation=mytology.data_creation,
            last_update=mytology.last_update,
            main_symbol=mytology.main_symbol,
            mytology_banner=mytology.mytology_banner,
            mytology_profile_img=mytology.mytology_profile_img,
            stories=story_list,
            comments=comments_list
        )
        mytology_list.append(mytology_read)

    return MytologyReadList(mytologies=mytology_list)

@router.get('/{mythology_id}', response_model=MytologyRead)
def read_mytology(mythology_id: int):
    mytology = MytologyDB.get_or_none(MytologyDB.id == mythology_id)
    if not mytology:
        raise HTTPException(status_code=404, detail="Mythology not found")

    comments = mytology.comments
    comments_list = [CommentRead.from_orm(comment) for comment in comments]

    mytology_read = MytologyRead.from_orm(mytology)
    mytology_read.comments = comments_list

    return mytology_read

@router.delete('/{mythology_id}', response_model=MytologyRead)
def delete_mytology(mythology_id: int):
    mytology = MytologyDB.get_or_none(MytologyDB.id == mythology_id)
    if not mytology:
        raise HTTPException(status_code=404, detail="Mythology not found")
    mytology.delete_instance()
    return MytologyRead.from_orm(mytology)

app.include_router(router)
