from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

deposit = InlineKeyboardMarkup(row_width=2)

btn = InlineKeyboardButton(text='Пополнить', callback_data='payment')
deposit.add(btn)