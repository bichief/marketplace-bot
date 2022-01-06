import asyncio


from utils.db_api.base import engine, Base


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
