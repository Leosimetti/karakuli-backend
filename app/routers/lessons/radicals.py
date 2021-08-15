from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.depends import get_current_user, get_db_session
from app.models import User, Radical
from app.schemas.radical import RadicalCreate
from app.scrapper import radicals

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
    # Todo @todo check if already exists, as has to be unique
    radical = await Radical.create(session, rad)

    return radical

# Todo @todo PLZ DO NOT FORGET TO REMOVE THIS IN PROD OR YOU ARE RETARD
import os

if os.getenv("IS_DEV"):
    @api.post(
        "/parse",
        status_code=status.HTTP_200_OK,
    )
    async def parse(
            no_variations: bool = False,
            session: AsyncSession = Depends(get_db_session),
    ):
        if await Radical.get_by_radical(session, "⼀"):  # Todo @todo remove this retarded if
            return "Already parsed"
        else:
            gen = radicals(no_variations=no_variations)
            for _ in range(50):
                w = next(gen)
                await Radical.create(session, dict=w)

        return "Done"
