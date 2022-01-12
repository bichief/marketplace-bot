from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import config

cmd_help = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(text='Правила', url=config.URL_RULES)
    ],
    [
        InlineKeyboardButton(text='Поддержка', url='t.me/nedire')
    ],
    [
        InlineKeyboardButton(text='Канал', url=config.URL_CHANNEL)
    ]
])