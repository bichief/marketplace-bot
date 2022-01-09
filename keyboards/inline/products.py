from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import utils.db_api.commands.goods as db


async def markup():
    products = InlineKeyboardMarkup(row_width=2)

    array = await db.get_category()

    for row in array:
        btn = InlineKeyboardButton(text=f'{row}', callback_data=f'category_{row}')
        products.add(btn)
    return products