import asyncio
import time

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from handlers.users.menu import menu_cmd
from keyboards.inline.on_start import on_start
from keyboards.inline.sub_channel import sub_channel
from loader import dp, bot
from utils.check_member import check_member
import utils.db_api.commands.user as db

from utils.delete_message import delete_message
from utils.misc import rate_limit


@dp.message_handler(CommandStart())
@rate_limit(2, 'start')
async def bot_start(message: types.Message):
    state = await db.add_user(telegram_id=message.chat.id, username=f'@{message.from_user.username}')
    if state is True:
        await message.answer('👨‍🔧 Вы уже ввели /start.')
    else:
        msg = await message.answer('👮‍♀️')
        asyncio.create_task(delete_message(msg, 0.57))
        time.sleep(2)
        await message.answer(f'🙋 Здравствуйте, {message.from_user.first_name}!\n'
                             f'👨‍💻 Перед началом использования бота, необходимо <b>ознакомиться с правилами</b> и <b>подписаться на канал</b>.',
                             reply_markup=on_start)


@dp.callback_query_handler(text='rules')
async def get_rules(call: types.CallbackQuery):
    await bot.edit_message_text(
        text='🙆 Для ознакомления с правилами, нажмите на кнопку ниже.\n\n'
             '<span class="tg-spoiler">👨‍🔧 Сообщение для владельцев iPhone:\n'
             'для того, чтобы кнопки заработали, введите команду /start еще раз</span>',
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=sub_channel,

    )


@dp.callback_query_handler(text='check_sub')
async def check_sub(call: types.CallbackQuery):
    state = await check_member(user_id=call.message.chat.id)
    if state is True:
        await bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
        await call.answer('👨‍🔧 Ваша подписка найдена!')
        await menu_cmd(call.message)
    else:
        await call.answer(call.message.chat.id, '👨‍🔧 Ваша подписка не найдена!')
