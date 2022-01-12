from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import config

sub_channel = InlineKeyboardMarkup(row_width=2,
                                   inline_keyboard=[
                                       [
                                            InlineKeyboardButton(text='❕Правила', url=config.URL_RULES)
                                       ],
                                       [
                                           InlineKeyboardButton(text='📍 Подписаться', url=config.URL_CHANNEL),
                                           InlineKeyboardButton(text='🔍 Проверить', callback_data='check_sub')
                                       ]
                                   ])
