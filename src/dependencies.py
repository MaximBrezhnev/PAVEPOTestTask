from typing import Generator, Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import database_settings


async def get_db_session() -> Generator[AsyncSession, Any, None]:
    try:
        session: AsyncSession = database_settings.async_session()
        yield session
    finally:
        await session.close()
