from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.depends import get_db_session, get_current_user
from app.models import User, StudyList

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
    # Todo extract code from the function
    return await StudyList.get_n_new_words(session, user.current_list_id, user.id, n)  # tODO take user into account
