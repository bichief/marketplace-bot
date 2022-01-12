from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import config

rules_url = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(text='❕ Правила', url=config.URL_RULES)
    ]
])