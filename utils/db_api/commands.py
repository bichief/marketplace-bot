from sqlalchemy.exc import IntegrityError

from loader import bot
from utils.db_api.base import async_session
from utils.db_api.classes_for_cmd import UserAdd


async def add_user(telegram_id, username):
    try:
        async with async_session() as session:
            async with session.begin():
                user = UserAdd(session)
                return await user.add_user(telegram_id, username)
    except IntegrityError:
        await bot.send_message(telegram_id, 'Вы уже авторизовались в боте.')
        return True
