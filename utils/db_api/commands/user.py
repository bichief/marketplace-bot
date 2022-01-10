from sqlalchemy import update, select, func
from sqlalchemy.exc import IntegrityError

from utils.db_api.base import async_sessionmaker
from utils.db_api.models.balance import Balance
from utils.db_api.models.user import User


async def add_user(telegram_id, username):
    try:
        async with async_sessionmaker() as session:
            await session.merge(User(telegram_id=telegram_id, username=username))
            await session.commit()
    except IntegrityError:
        return True


async def update_state(telegram_id):
    async with async_sessionmaker() as session:
        state = (
            update(User).where(User.telegram_id == telegram_id).values(state='true')
        )

        await session.execute(state)
        await session.commit()

async def get_info(telegram_id):
    array = []
    async with async_sessionmaker() as session:
        info = select(User).where(User.telegram_id == telegram_id)

        result = await session.execute(info)

        for row in result.scalars():
            array.append(row.id)
            data = str(row.created_at).split(' ')[0]
            array.append(data)
        return array


async def get_all_users():

    async with async_sessionmaker() as session:
        counter = select(func.count('*')).select_from(User)
        result = await session.execute(counter)
        for row in result:
            return row[0]

async def get_users_for_txt():
    array = []
    async with async_sessionmaker() as session:
        sql = select(User)
        result = await session.execute(sql)
        for row in result.scalars():
            array.append(f'{row.telegram_id} - {row.username}')
        return array

async def get_all_users_mailing():
    array = []
    async with async_sessionmaker() as session:
        sql = select(User)
        result = await session.execute(sql)
        for row in result.scalars():
            array.append(row.telegram_id)
        return array