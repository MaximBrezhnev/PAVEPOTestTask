from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db_session
from src.sender.services.services import SenderService


def get_service(
    db_session: AsyncSession = Depends(get_db_session),
) -> SenderService:

    return SenderService(
        db_session=db_session,
    )
