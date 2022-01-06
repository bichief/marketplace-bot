import time

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import ChatActions

from keyboards.default.menu import menu
from keyboards.inline.history import history
from loader import dp, bot



@dp.message_handler(Command('menu'))
async def menu_cmd(message: types.Message):

    await message.answer('На данный момент вы находитесь в меню.\n\n'
                         'Выберите на клавиатуре то, в чем вы заинтересованы', reply_markup=menu)


@dp.message_handler(text='Товары')
async def goods(message: types.Message):
    await message.answer('text')


@dp.message_handler(text='Профиль')
async def user_profile(message: types.Message):
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    time.sleep(1.2)
    data = 'text'
    await message.answer('<b>Ваш профиль.</b>\n\n'
                         f'Юзернейм: @{message.from_user.username}\n'
                         f'Баланс: balance\n'
                         f'Дата подключения: {data}\n',
                         reply_markup=history)


@dp.message_handler(text='Баланс')
async def user_balance(message: types.Message):
    pass  # систему с инлайн кнопками


@dp.message_handler(text='Авторизация')
async def login(message: types.Message):
    pass  # регистрация для чего-нить, хз)


@dp.message_handler(text='Поддержка')
async def support(message: types.Message):
    pass  # линк на саппорта


@dp.message_handler(text='Правила')
async def rules(message: types.Message):
    pass  # выдает правила
