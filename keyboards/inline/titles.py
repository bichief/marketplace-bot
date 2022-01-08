from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.commands import get_name


async def titles(rows):

    markup = InlineKeyboardMarkup(row_width=2)

    for row in rows:
        row = row.split(':')
        title = await get_name(row[0])

        btn = InlineKeyboardButton(text=f'{row[1]}', callback_data=f'id_{title}')

        markup.add(btn)
    cancel = InlineKeyboardButton(text='<< К категориям', callback_data='menu')
    markup.add(cancel)
    return markup