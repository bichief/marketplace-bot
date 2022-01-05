from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

sub_channel = InlineKeyboardMarkup(row_width=3,
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(text='Подписаться на канал', url='t.me/bichief'),
                                           InlineKeyboardButton(text='Проверить подписку', callback_data='check_sub')
                                       ]
                                   ])