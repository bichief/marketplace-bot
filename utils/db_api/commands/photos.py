import random
from sqlalchemy import select

from utils.db_api.base import async_sessionmaker
from utils.db_api.models.goods import Goods
from utils.db_api.models.photo import GoodsPhoto


async def insert_photo(good_id, photo_url=''):
    async with async_sessionmaker() as session:
        ID = random.randint(1, 1000)
        await session.merge(GoodsPhoto(id=ID, goods_id=int(good_id), url=photo_url))
        await session.commit()


async def get_photo(good_id):
    async with async_sessionmaker() as session:

        photo = select(GoodsPhoto).where(GoodsPhoto.goods_id == int(good_id))

        result = await session.execute(photo)

        for row in result.scalars():
            return row.url
