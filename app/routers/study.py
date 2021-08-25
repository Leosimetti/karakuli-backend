from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.depends import get_current_user, get_db_session
from app.models import StudyList, User

api = APIRouter(tags=["Study"], prefix="/study")


@api.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def list_n_current_user_study_items(
    n: int,
    session: AsyncSession = Depends(get_db_session),
    user: User = Depends(get_current_user()),
):
    # Todo @todo extract code from the function
    return await StudyList.get_n_new_words(session, user.current_list_id, user.id, n)
