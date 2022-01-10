import aiofiles
import os

from utils.db_api.commands.goods import get_all_goods
from utils.db_api.commands.user import get_users_for_txt


async def insert_txt():
    rows = await get_all_goods()

    if os.path.exists('goods.txt'):
        os.remove('goods.txt')

    async with aiofiles.open('goods.txt', mode='a', encoding='utf-8') as f:
        for row in rows:
            await f.write(row)
            await f.write('\n')
        f.close()

async def insert_balance_txt():
    rows = await get_users_for_txt()

    if os.path.exists('users.txt'):
        os.remove('users.txt')

    async with aiofiles.open('users.txt', mode='a', encoding='utf-8') as f:
        for row in rows:
            await f.write(row)
            await f.write('\n')
        f.close()
