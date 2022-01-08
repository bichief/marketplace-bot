from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from utils.db_api.base import engine
from utils.db_api.schemas.balance import Balance
from utils.db_api.schemas.goods import Goods
from utils.db_api.schemas.user import User
from sqlalchemy import update, select

async_sessionmaker = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def add_user(telegram_id, username):
    try:
        db_session = async_sessionmaker
        async with db_session() as session:
            await session.merge(User(telegram_id=telegram_id, username=username))
            await session.commit()
    except IntegrityError:
        return True


async def update_state(telegram_id):
    db_session = async_sessionmaker
    async with db_session() as session:
        state = (
            update(User).where(User.telegram_id == telegram_id).values(state='true')
        )

        await session.execute(state)
        await session.commit()


async def create_balance(telegram_id):
    try:
        global user_id
        db_session = async_sessionmaker

        async with db_session() as session:
            await session.merge(Balance(telegram_id=telegram_id))
            await session.commit()
    except IntegrityError:
        pass


async def get_info(telegram_id):
    db_session = async_sessionmaker
    array = []
    async with db_session() as session:
        info = select(User).where(User.telegram_id == telegram_id)

        result = await session.execute(info)

        for row in result.scalars():
            array.append(row.id)
            data = str(row.created_at).split(' ')[0]
            array.append(data)
        return array


async def get_balance(telegram_id):
    db_session = async_sessionmaker

    async with db_session() as session:
        balance = select(Balance).where(Balance.telegram_id == telegram_id)

        result = await session.execute(balance)

        for row in result.scalars():
            return row.amount


async def get_category():
    try:
        array = []

        db_session = async_sessionmaker

        async with db_session() as session:
            category = select(Goods.category)

            result = await session.execute(category)

            for row in result.scalars():
                if row not in array:
                    array.append(row)

            return array
    except IntegrityError:
        pass


async def check_rows():
    rows = await get_category()
    if len(rows) == 0:
        return True
    else:
        return rows


async def get_title(category):
    try:
        array = []
        titleused = []

        db_session = async_sessionmaker

        async with db_session() as session:
            goods = select(Goods).where(Goods.category == category)

            result = await session.execute(goods)

            for row in result.scalars():
                titleused.append(row.title)
                array.append(f'{row.id}: {row.title} - {row.price} RUB - {row.amount} шт.')

            merchant = []

            for row in array:
                regex = row.split(':')
                regex = regex[1].split(' ')

                merchant.append(f'{row}')
            return merchant
    except IntegrityError:
        pass


async def get_name(goods_id):
    db_session = async_sessionmaker

    async with db_session() as session:
        name = select(Goods).where(Goods.id == int(goods_id))

        result = await session.execute(name)
        for row in result.scalars():
            return row.title
