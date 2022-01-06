import asyncio
import time

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from handlers.users.menu import menu_cmd
from keyboards.inline.on_start import on_start
from keyboards.inline.sub_channel import sub_channel
from loader import dp, bot
from utils.check_member import check_member
from utils.db_api.commands import add_user
from utils.delete_message import delete_message


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await add_user(telegram_id=message.chat.id, username=f'@{message.from_user.username}')
    # if state is True:
    #     pass
    # else:
    msg = await message.answer('👮‍♀️')
    asyncio.create_task(delete_message(msg, 0.57))
    time.sleep(2)
    await message.answer(f'🙋Доброго времени суток, {message.from_user.first_name}!\n\n'
                         f'🙆Для начала работы со мной, вам необходимо <b>ознакомиться с правилами</b> площадки и <b>подписаться</b> на канал.',
                         reply_markup=on_start)


@dp.callback_query_handler()
async def get_rules(call: types.CallbackQuery):
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

            await call.answer('Ваша подписка найдена!')
            await menu_cmd(call.message)
        else:
            await bot.send_message(call.message.chat.id, 'Ваша подписка не найдена!')
