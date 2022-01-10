from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

mailing_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Сообщение')
    ],
    [
        KeyboardButton(text='Сообщение с картинкой')
    ],
    [
        KeyboardButton(text='Голосовое сообщение')
    ],
    [
        KeyboardButton(text='Видео "кружочек"')
    ],

    [
        KeyboardButton(text='Текст с кнопкой')
    ],
    [
        KeyboardButton(text='Назад')
    ]
])
