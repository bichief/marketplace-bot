from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_payment(url):
    markup = InlineKeyboardMarkup(row_width=2)

    btn = InlineKeyboardButton(text='Пополнить', url=url)
    btn2 = InlineKeyboardButton(text='Проверить оплату', callback_data='check_payment')
    markup.add(btn, btn2)
    return markup