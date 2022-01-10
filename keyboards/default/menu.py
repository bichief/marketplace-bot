from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3,
                           keyboard=[
                               [
                                   KeyboardButton(text='🙆Товары'),
                                   KeyboardButton(text='Профиль'),
                                   KeyboardButton(text='Баланс')
                               ],
                               [
                                   KeyboardButton(text='Авторизация'),
                                   KeyboardButton(text='Поддержка'),
                                   KeyboardButton(text='Правила')
                               ]
                           ])
