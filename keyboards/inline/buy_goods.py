from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def buy_goods(ID, SUM):
    markup = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [
            InlineKeyboardButton(text='Приобрести товар', callback_data=f'buy_{ID}_{SUM}')
        ],
        [
            InlineKeyboardButton(text='<< Назад', callback_data='back')
        ]
    ])
    return markup