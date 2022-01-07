from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from utils.db_api.base import get_session, engine
from utils.db_api.schemas.user import User


async def add_user(telegram_id, username):
    try:
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )

        async with async_session() as session:
            async with session.begin():
                user = User(telegram_id=telegram_id, username=username)
                session.add(user)
                await session.commit()
    except IntegrityError:
        return True
