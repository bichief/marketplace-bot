from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from utils.db_api.base import async_sessionmaker
from utils.db_api.schemas.balance import Balance


async def create_balance(telegram_id):
    try:

        async with async_sessionmaker() as session:
            await session.merge(Balance(telegram_id=telegram_id))
            await session.commit()
    except IntegrityError:
        pass

async def get_balance(telegram_id):
    async with async_sessionmaker() as session:
        balance = select(Balance).where(Balance.telegram_id == telegram_id)

        result = await session.execute(balance)

        for row in result.scalars():
            return row.amount