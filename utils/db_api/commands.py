from sqlalchemy.ext.asyncio import AsyncSession

from utils.db_api.base import get_session
from utils.db_api.schemas.user import User


async def add_user(telegram_id, username, session: AsyncSession = get_session()):
    user = User(telegram_id=telegram_id, username=username)
    session.add(user)
    await session.commit()
