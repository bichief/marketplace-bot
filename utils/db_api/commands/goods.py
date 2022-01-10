from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from utils.db_api.base import async_sessionmaker
from utils.db_api.models.goods import Goods
from utils.db_api.models.photo import GoodsPhoto


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
            return [row.title, row.amount]


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

async def insert_goods(good_id, category, title, desc, data, price, amount):
    async with async_sessionmaker() as session:
        await session.merge(Goods(id=good_id, category=category, title=title, description=desc, data=data, price=price, amount=amount))
        await session.commit()

async def get_all_goods():
    array = []
    async with async_sessionmaker() as session:
        data = select(Goods)

        result = await session.execute(data)

        for row in result.scalars():
            array.append(f'{row.id}: {row.category} - {row.title} - {row.description} - {row.price} - {row.amount}')
        return array

async def delete_goods_id(id: int):
    async with async_sessionmaker() as session:
        bye = delete(Goods).where(Goods.id == int(id))
        bye_bye = delete(GoodsPhoto).where(GoodsPhoto.goods_id == int(id))
        await session.execute(bye_bye)
        await session.execute(bye)
        await session.commit()

async def update_price(id, price):
    async with async_sessionmaker() as session:
        sql = update(Goods).where(Goods.id == id).values(price=price)
        await session.execute(sql)
        await session.commit()