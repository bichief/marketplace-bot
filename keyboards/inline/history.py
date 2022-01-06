from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

history = InlineKeyboardMarkup(row_width=1,
                               inline_keyboard=[
                                   [
                                       InlineKeyboardButton(text='История покупок', callback_data='history')
                                   ],
                                   [
                                       InlineKeyboardButton(text='Beta', callback_data='beta')
                                   ]
                               ])
