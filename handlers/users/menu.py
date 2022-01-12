import time
import random

from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ChatActions

from data import config
from handlers.users.balance import balance_cmd
from keyboards.default.menu import menu
from keyboards.inline.buy_goods import buy_goods
from keyboards.inline.products import markup
from keyboards.inline.rules_link import rules_url
from keyboards.inline.support_link import support_link
from keyboards.inline.titles import titles
from keyboards.inline.url import url
from loader import dp, bot

import utils.db_api.commands.goods as db
import utils.db_api.commands.balance as bl
import utils.db_api.commands.user as us
import utils.db_api.commands.photos as ph


@dp.message_handler(Command('set_menu'), user_id=config.ADMINS)
async def menu_cmd(message: types.Message):
    await us.update_state(telegram_id=message.chat.id)
    await bl.create_balance(telegram_id=message.chat.id)
    await message.answer('🙋‍♀️ Добро пожаловать в меню!\n'
                         '🙆‍♀️ Для взаимодействия, используйте клавиатуру, расположенную ниже.', reply_markup=menu)


@dp.message_handler(text='🙆Товары')
async def goods(message: types.Message):
    if await db.check_rows() is True:
        await message.answer('👨‍🔧 К сожалению, категории товаров пока недоступны.')
    else:
        keyboard = await markup()
        await message.answer('👩‍💻 Перед вами доступные категории товаров.', reply_markup=keyboard)


@dp.message_handler(text='💁Профиль')
async def user_profile(message: types.Message):
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    time.sleep(1.2)
    data = await us.get_info(telegram_id=message.chat.id)
    balance = await bl.get_balance(telegram_id=message.chat.id)
    username = message.from_user.username
    if username is None:
        username = 'не указан :('
    await message.answer(f'<b>🙆‍♀️ Ваш профиль.</b>\n\n'
                         f'📌 Ваш никнейм: <b>{username}</b>\n'
                         f'💰 Ваш баланс: <code>{balance} RUB</code>\n'
                         f'📅 Дата присоеденения: <b>{data[1]}</b>')


@dp.message_handler(text='💆Баланс')
async def user_balance(message: types.Message):
    await balance_cmd(message)


@dp.message_handler(text='🙅Авторизация')
async def login(message: types.Message):
    await message.answer('👨‍🔧 В разработке :)\n'
                         'Следи за новостями в канале.\n',
                         reply_markup=url)


@dp.message_handler(text='🤷Поддержка')
async def support(message: types.Message):
    await message.answer('🙋‍♀️ Невалидный товар? Что-то пошло не так?\n'
                         '👨‍🔧 Обратись к нашему Агенту, он обязательно тебе поможет!', reply_markup=support_link)


@dp.message_handler(text='🙍Правила')
async def rules(message: types.Message):
    await message.answer('🧑‍💻 Актуальные правила доступны по ссылке.', reply_markup=rules_url)


@dp.callback_query_handler(Text(startswith='category_'))
async def get_category(call: types.CallbackQuery):
    regex = call.data.split('_')
    rows = await db.get_title(regex[1])

    if len(rows) == 0:
        await bot.send_message(call.message.chat.id, f'👨‍🔧 К сожалению товары с категорией <b>{regex[1]}</b> отсутствуют.')
    else:
        keyboard = await titles(rows)
        await bot.edit_message_text('🙋‍♀ Перед вами доступные товары.', chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='id_'))
async def get_good(call: types.CallbackQuery):
    regex = call.data.split('_')
    rows = await db.get_goods_id(regex[1])
    goods_id = random.choice(rows)

    info = await db.get_info_goods(goods_id)

    if info is None:
        await bot.send_message(call.message.chat.id, '👨‍🔧 К сожалению, товар не найден.')
    else:
        row = info.split('&')

        ID = row[3]
        print(ID)
        SUM = row[2]
        print(SUM)
        photo = await ph.get_photo(ID)
        keyboard = await buy_goods(ID, SUM)

        if photo is None or photo == 'None':
            await bot.send_message(chat_id=call.message.chat.id,
                                   text=f'📝 Оформление заказа <b>№{random.randint(1000, 1000000)}</b>\n\n'
                                        f'✏️ Наименование: <b>{row[0]}</b>\n'
                                        f'🎫 Описание: {row[1]}\n\n'
                                        f'💵 Цена: <b>{row[2]} RUB</b>\n',
                                   reply_markup=keyboard)
        else:
            await bot.send_photo(chat_id=call.message.chat.id,
                                 caption=f'📝 Оформление заказа <b>№{random.randint(1000, 1000000)}</b>\n\n'
                                         f'✏️Наименование: <b>{row[0]}</b>\n'
                                         f'🎫 Описание: <b>{row[1]}</b>\n\n'
                                         f'💵 Цена: <b>{row[2]} RUB</b>\n',
                                 reply_markup=keyboard,
                                 photo=photo)


@dp.callback_query_handler(Text(equals='menu'))
async def go_back(call: types.CallbackQuery):
    keyboard = await markup()
    await call.message.answer('👩‍💻 Перед вами доступные категории товаров.', reply_markup=keyboard)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(Text(equals='back'))
async def go_category(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(Text(startswith='buy_'))
async def buy_product(call: types.CallbackQuery):
    regex = call.data.split('_')

    good_id = regex[1]

    summa = int(regex[2])

    balance = await bl.get_balance(telegram_id=call.message.chat.id)

    if int(balance) >= int(summa):

        data = await db.get_data_goods(good_id)

        info = await db.get_info_goods(good_id)
        rows = info.split('&')
        amount = rows[4]

        new_balance = balance - summa
        await bl.update_for_user(telegram_id=call.message.chat.id, amount=new_balance)
        new_amount = int(amount) - 1
        await db.update_amount(good_id, amount=new_amount)

        await bot.send_message(
            chat_id=call.message.chat.id,
            text='✅ Покупка успешно проведена!\n\n'
                 f'👩‍💻 Данные: {data}\n'
                 f'💰 Ваш баланс - {new_balance} RUB'
        )

    else:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='❌ Недостаточно средств на балансе.\n'
                 f'👨‍🔧 Для покупки вам не хватает {summa - balance} RUB\n'
        )
