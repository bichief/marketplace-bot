from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import config

url = InlineKeyboardMarkup(row_width=1)

link = InlineKeyboardButton(text='Перейти в канал', url=config.URL_CHANNEL)
url.add(link)
