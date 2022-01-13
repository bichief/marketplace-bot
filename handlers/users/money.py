import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from states.fake import Fake


@dp.message_handler(Command('update_balance'))
async def fake_money(message: types.Message):
    await message.answer('👨‍🔧 Отправьте мне сумму, для обновления баланса!')
    await Fake.first.set()


@dp.message_handler(state=Fake.first)
async def update_money(message: types.Message, state: FSMContext):
    await state.reset_state()

    amount = message.text
    time.sleep(5)

    await message.edit_text(f'Успешно!\n'
                            f'Баланс пользователя {message.chat.id} пополнен на {amount} RUB!')
