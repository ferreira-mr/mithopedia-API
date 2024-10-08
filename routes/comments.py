from fastapi import APIRouter, HTTPException

from models import CommentsDB, GodsDB, HistoryDB, MytologyDB, UserDB
from schemas import CommentCreate, CommentRead, CommentReadList

router = APIRouter(prefix='/comments', tags=['COMMENTS'])


@router.post('/', response_model=CommentRead)
async def create_comment(new_comment: CommentCreate):

    user = UserDB.get_or_none(UserDB.id == new_comment.id_user)
    god = GodsDB.get_or_none(GodsDB.id == new_comment.god_id)
    mytolog = MytologyDB.get_or_none(MytologyDB.id == new_comment.mytology_id)
    history = HistoryDB.get_or_none(HistoryDB.id == new_comment.history_id)

    comment = CommentsDB.create(
        comment=new_comment.comment,
        date=new_comment.date,
        last_update=new_comment.last_update,
        likes=new_comment.likes,
        status=new_comment.status,
        user=user,
        god=god,
        mytology=mytolog,
        history=history,
    )
    return comment


@router.put('/{comment_id}', response_model=CommentRead)
async def update_comment(comment_id: int, new_comment: CommentCreate):

    comment = CommentsDB.get_or_none(CommentsDB.id == comment_id)

    if comment is None:
        raise HTTPException(status_code=404, detail='Comment not found')

    for field, value in new_comment.dict(exclude_unset=True).items():
        setattr(comment, field, value)

    comment.save()

    return comment


@router.get('/', response_model=CommentReadList)
def list_comments():

    comments = CommentsDB.select()

    return {'comments': comments}


@router.get('/{comment_id}', response_model=CommentRead)
def read_comment(comment_id: int):

    comment = CommentsDB.get_or_none(CommentsDB.id == comment_id)

    if not comment:
        raise HTTPException(status_code=404, detail='Comment not found')

    return comment
