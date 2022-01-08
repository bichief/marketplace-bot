from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.commands import get_category, check_rows

async def markup():
    products = InlineKeyboardMarkup(row_width=2)

    array = await get_category()

    for row in array:
        btn = InlineKeyboardButton(text=f'{row}', callback_data=f'category_{row}')
        products.add(btn)
    return products