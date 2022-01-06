import asyncio
import logging

from sqlalchemy.ext.asyncio import create_async_engine

from data import config
from utils.db_api.base import Base


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    engine = create_async_engine(config.DB_LINK, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())