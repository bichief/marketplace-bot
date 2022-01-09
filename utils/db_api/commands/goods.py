from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from utils.db_api.base import async_sessionmaker
from utils.db_api.schemas.goods import Goods


async def get_category():
    try:
        array = []

        async with async_sessionmaker() as session:
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

        async with async_sessionmaker() as session:
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
    async with async_sessionmaker() as session:
        name = select(Goods).where(Goods.id == int(goods_id))

        result = await session.execute(name)
        for row in result.scalars():
            return row.title


async def get_goods_id(title):
    array = []

    async with async_sessionmaker() as session:
        numbers = select(Goods.id).where(Goods.title == title)

        result = await session.execute(numbers)
        for row in result.scalars():
            array.append(row)
        return array


async def get_info_goods(good_id):
    async with async_sessionmaker() as session:
        info = select(Goods).where(Goods.id == int(good_id))

        result = await session.execute(info)

        for row in result.scalars():
            return f'{row.title}:{row.description}:{row.price}:{row.id}:{row.amount}'

async def get_data_goods(good_id):
    async with async_sessionmaker() as session:
        data = select(Goods).where(Goods.id == int(good_id))

        result = await session.execute(data)
        for row in result.scalars():
            return row.data

async def update_amount(good_id, amount: int):
    async with async_sessionmaker() as session:
        new_amount = update(Goods).where(Goods.id == int(good_id)).values(amount=amount)

        await session.execute(new_amount)
        await session.commit()