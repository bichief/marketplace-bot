import time

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import ChatActions

from keyboards.default.menu import menu
from keyboards.inline.history import history
from keyboards.inline.products import markup
from keyboards.inline.sub_channel import sub_channel
from keyboards.inline.titles import titles
from loader import dp, bot
from utils.check_member import check_member
from utils.db_api.commands import update_state, get_info, create_balance, get_balance, get_category, check_rows, \
    get_title


@dp.message_handler(Command('menu'))
async def menu_cmd(message: types.Message):
    await update_state(telegram_id=message.chat.id)
    await create_balance(telegram_id=message.chat.id)
    await message.answer('На данный момент вы находитесь в меню.\n\n'
                         'Выберите на клавиатуре то, в чем вы заинтересованы', reply_markup=menu)


@dp.message_handler(text='Товары')
async def goods(message: types.Message):
    if await check_rows() is True:
        await message.answer('К сожалению, категории пока недоступны.')
    else:
        keyboard = await markup()
        await message.answer('Доступные категории товаров:', reply_markup=keyboard)


@dp.message_handler(text='Профиль')
async def user_profile(message: types.Message):
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    time.sleep(1.2)
    data = await get_info(telegram_id=message.chat.id)
    balance = await get_balance(telegram_id=message.chat.id)
    await message.answer('<b>Ваш профиль.</b>\n\n'
                         f'ID: {data[0]} \n'
                         f'Баланс: <code>{balance} RUB</code>\n'
                         f'Дата подключения: {data[1]}\n',
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


@dp.callback_query_handler()
async def get_goods(call: types.CallbackQuery):
    if 'rules' in call.data:
        await bot.edit_message_text(
            text='правила придумать потом',
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=sub_channel
        )
    if 'check_sub' in call.data:
        state = await check_member(user_id=call.message.chat.id)
        if state is True:
            await bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
            await call.answer('Ваша подписка найдена!')
            await menu_cmd(call.message)
        else:
            await bot.send_message(call.message.chat.id, 'Ваша подписка не найдена!')

    if 'category_' in call.data:
        regex = call.data.split('_')
        rows = await get_title(regex[1])

        if len(rows) == 0:
            await bot.send_message(call.message.chat.id, f'К сожалению товары с категорией {regex[1]} отсутствуют :(')
        else:
            keyboard = await titles(rows)
            await bot.edit_message_text('Товары!', chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        reply_markup=keyboard)
    elif 'menu' in call.data:
        keyboard = await markup()
        await call.message.answer('Доступные категории товаров:', reply_markup=keyboard)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

