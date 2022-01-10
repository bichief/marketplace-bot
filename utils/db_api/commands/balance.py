from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from utils.db_api.base import async_sessionmaker
from utils.db_api.models.balance import Balance


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

async def update_for_user(telegram_id, amount: int):
    async with async_sessionmaker() as session:
        balance = update(Balance).where(Balance.telegram_id == telegram_id).values(amount=amount)

        await session.execute(balance)
        await session.commit()

async def update_by_user(telegram_id, amount: int):
    sql = select(Balance).where(Balance.telegram_id == telegram_id)
    async with async_sessionmaker() as session:
        process_execute = await session.execute(sql)
        for row in process_execute.scalars():
            old_balance = row.amount

        new_balance = int(old_balance) + int(amount)

        balance = update(Balance).where(Balance.telegram_id == telegram_id).values(amount=new_balance)

        await session.execute(balance)
        await session.commit()