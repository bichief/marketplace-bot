import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp, bot
from states.fake import Fake


@dp.message_handler(Command('update_balance'))
async def fake_money(message: types.Message):
    await message.answer('👨‍🔧 Отправьте мне сумму, для обновления баланса!')
    await Fake.first.set()


@dp.message_handler(state=Fake.first)
async def update_money(message: types.Message, state: FSMContext):
    await state.reset_state()
    amount = message.text
    await message.answer(f'👨‍🔧 Хорошо, сумма обновлена баланса равна {amount}\n'
                         f'Начинаю подключаться к Базе Данных.')
    time.sleep(2.5)
    time.sleep(2)
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text='👨‍🔧 Подключение к БД\n'
             'DB_NAME: <b>market</b>\n'
             'DB_HOST: <b>hidden</b>\n'
             'SQL: <b>UPDATE market_balances WHERE id == %1, (%1=message.chat.id)</b>'
    )
    time.sleep(2)
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text='👨‍🔧 Подключение к БД - <b>SUCCESSFUL</b>✅')

    text = '☐☐'

    square = '☐'

    seconds = 1.5

    for i in range(5):
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text='👨‍🔧 Отправляю запрос, <b>состояние</b>:\n\n'
                 f'{text}'
        )
        time.sleep(2+seconds)
