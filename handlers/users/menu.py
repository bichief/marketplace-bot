from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.default.menu import menu
from loader import dp, bot
from utils.check_member import check_member
from utils.misc import rate_limit


@dp.message_handler(Command('menu'))
async def menu_cmd(message: types.Message):
    await message.answer('На данный момент вы находитесь в меню.\n\n'
                         'Выберите на клавиатуре то, в чем вы заинтересованы', reply_markup=menu)


@dp.message_handler(text='Товары')
async def goods(message: types.Message):
    pass


@dp.message_handler(text='Профиль')
async def user_profile(message: types.Message):
    pass  # информация баланс, дата регистрации, история покупок


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
