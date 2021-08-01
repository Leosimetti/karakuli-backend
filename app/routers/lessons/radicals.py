from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.depends import get_current_user, get_db_session
from app.models import User, Radical
from app.schemas.radical import RadicalCreate

api = APIRouter(tags=["Radicals"], prefix="/radicals")


@api.post(
    "",
    status_code=status.HTTP_200_OK,
)
async def add(
        rad: RadicalCreate,
        session: AsyncSession = Depends(get_db_session),
        _: User = Depends(get_current_user())
):

    # Todo check if already exists, as has to be unique
    radical = await Radical.create(session, rad)

    return radical
