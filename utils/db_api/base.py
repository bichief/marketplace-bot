from aiogram import Dispatcher
from sqlalchemy.orm import declarative_base, sessionmaker
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from data import config

Base = declarative_base()

engine = create_async_engine(config.DB_LINK, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def connect_db(dispatcher: Dispatcher):
    print("Connection to PostgreSQL")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
