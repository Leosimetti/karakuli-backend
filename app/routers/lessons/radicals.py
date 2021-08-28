import os
from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.depends import get_current_user, get_db_session
from app.models import Radical, User
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
    _: User = Depends(get_current_user()),
):
    # Todo @todo check if already exists, as has to be unique
    radical = await Radical.create(session, rad)

    return radical


# Todo @todo PLZ DO NOT FORGET TO REMOVE THIS IN PROD OR YOU ARE RETARD

if os.getenv("IS_DEV"):

    @api.post(
        "/parse",
        status_code=status.HTTP_200_OK,
    )
    async def parse(
        amount: Optional[int] = 50,
        no_variations: bool = False,
        session: AsyncSession = Depends(get_db_session),
    ):

        if await Radical.get_by_radical(
            session, "⼀"
        ):  # Todo @todo remove this retarded if
            return "Already parsed"
        else:
            for _, k in zip(range(amount), radicals(no_variations=no_variations)):
                await Radical.create(session, dict=k)
        return "Done"
