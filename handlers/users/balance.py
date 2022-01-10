import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from data import config
from keyboards.inline.deposit import deposit
from keyboards.inline.payment import get_payment
from loader import dp, p2p, bot
from states.payment import NewPayment
from utils.db_api.commands.balance import get_balance, update_for_user


@dp.message_handler(Command('balance'), user_id=config.ADMINS)
async def balance_cmd(message: types.Message):
    amount = await get_balance(telegram_id=message.chat.id)
    await message.answer(f'Ваш баланс равен - {amount} RUB\n\n',
                         reply_markup=deposit)


@dp.callback_query_handler(Text(equals='payment'), state=None)
async def new_payment(call: types.CallbackQuery):
    await call.message.answer('Введите сумму пополнения\n\n'
                              'Минимальная сумма пополнения - 30 RUB')
    await NewPayment.first()


@dp.message_handler(state=NewPayment.amount)
async def order_payment(message: types.Message, state: FSMContext):
    amount = message.text
    if int(amount) < 3:
        await message.answer('Вы ошиблись.\n'
                             'Минимальная сумма пополнения - 30 RUB.\n\n'
                             'Попробуйте еще раз.')
        await NewPayment.first()
    else:
        await state.update_data(amount=amount)
        await state.update_data(bill_id=f'{random.randint(1,1000000)}')
        data = await state.get_data()
        price = data.get('amount')
        print(price, 'PRICE')
        bill_id = data.get('bill_id')
        bill = await p2p.bill(bill_id=bill_id, amount=int(price), lifetime=15)
        url = bill.pay_url
        keyboard = await get_payment(url)
        await message.answer('Вот ваша ссылка для пополнения', reply_markup=keyboard)
        await state.reset_state(with_data=False)

@dp.callback_query_handler(Text(equals='check_payment'))
async def check_payment(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    bill = data.get('bill_id')
    price = data.get('amount')
    print(bill, 'BILL ID')
    status = await p2p.check(bill_id=bill)
    if status.status == 'PAID':
        old_balance = await get_balance(telegram_id=call.message.chat.id)
        new_balance = int(old_balance) + int(price)
        await update_for_user(telegram_id=call.message.chat.id, amount=new_balance)
        await bot.send_message(call.message.chat.id, f'Ваш баланс успешно пополнен на {price} RUB.')
    elif status.status == 'WAITING':
        await bot.send_message(call.message.chat.id, 'Уведомлений об оплате пока что нет.\n'
                                                     'Если оплата не поступит в течении 15 минут, счет будет закрыт.')
    elif status.status == 'EXPIRED':
        await bot.send_message(call.message.chat.id, 'Счет был закрыт.\n'
                                                     'Для повторного пополнения баланса, воспользуйтесь кнопкой на клавиатуре.')