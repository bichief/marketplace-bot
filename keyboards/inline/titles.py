from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import utils.db_api.commands.goods as db


async def titles(rows):
    global data
    markup = InlineKeyboardMarkup(row_width=2)

    data = markup.inline_keyboard
    for row in rows:
        row = row.split(':')
        title = await db.get_name(row[0])

        if int(title[1]) <= 0:
            btn = InlineKeyboardButton(text='К сожалению, товар отсутствует.', callback_data='menu')
            markup.add(btn)
        else:
            btn = InlineKeyboardButton(text=f'{row[1]}', callback_data=f'id_{title[0]}')
            markup.add(btn)

    cancel = InlineKeyboardButton(text='<< К категориям', callback_data='menu')
    markup.add(cancel)
    return markup
