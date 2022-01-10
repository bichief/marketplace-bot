from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Пользователи')
    ],
    [
        KeyboardButton(text='Товары')
    ],
    [
        KeyboardButton(text='Рассылка')
    ],
    [
        KeyboardButton(text='Вернуться в меню')
    ]
])

users = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Количество')
    ],
    [
        KeyboardButton('Обновить баланс')
    ]
])

goods = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Добавить товар')
    ],
    [
        KeyboardButton(text='Удалить товар')
    ],
    [
        KeyboardButton(text='Изменить цену товара')
    ]
])

comeback = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Назад')
    ]
])
