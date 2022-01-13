import time
from datetime import timedelta, datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loader import dp, bot
from states.fake import Fake

scheduler = AsyncIOScheduler()
scheduler.start()


@dp.message_handler(Command('update_balance'))
async def fake_money(message: types.Message):
    await message.answer('👨‍🔧 Отправьте мне сумму, для обновления баланса!')
    await Fake.first.set()


@dp.message_handler(state=Fake.first)
async def update_money(message: types.Message, state: FSMContext):
    await state.reset_state()

    amount = message.text

    msg = await bot.send_message(chat_id=message.chat.id,
                                 text=f'👨‍🔧 Хорошо, сумма обновлена баланса равна {amount}\n'
                                      f'Начинаю подключаться к Базе Данных.')
    date = datetime.now() + timedelta(seconds=3)
    scheduler.add_job(edit_message, "date", run_date=date, kwargs={"message": msg})


async def edit_message(message: types.Message):
    new_msg = await message.edit_text(
        text='👨‍🔧 Подключение к БД\n'
             'DB_NAME: <b>market</b>\n'
             'DB_HOST: <b>hidden</b>\n'
             'SQL: <b>UPDATE market_balances WHERE id == %1, (%1=message.chat.id)</b>'
    )
    time.sleep(2)
    date = datetime.now() + timedelta(seconds=3)
    scheduler.add_job(edit_msg, name="next", run_date=date, kwargs={"message": new_msg})


async def edit_msg(message: types.Message):
    final = await message.edit_text(text='👨‍🔧 Подключение к БД - <b>SUCCESSFUL</b>✅')
    date = datetime.now() + timedelta(seconds=3)
    scheduler.add_job(edit_msg, name="next", run_date=date, kwargs={"message": final})
async def final_edit(message: types.Message):

    text = '☐☐'
    nothing = 123
    square = '☐'
    seconds = 1.5

    for i in range(5):
        if len(text) == 10:
            await message.edit_text(
                text='Готово!'
            )
        await message.answer(
            text='👨‍🔧 Отправляю запрос, <b>состояние</b>:\n\n'
                 f'{text}'
        )
        time.sleep(2 + seconds)
        text += square
