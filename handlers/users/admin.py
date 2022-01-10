import datetime
import time
import aiofiles

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BotBlocked, TypeOfFileMismatch

from data import config
from handlers.users.menu import menu_cmd
from keyboards.default.admin import admin, users, goods, comeback
from keyboards.default.mailing import mailing_keyboard
from loader import dp, bot
from states.admin import Admin
from states.delete_goods import DeleteGoods
from states.mailing import Mailing
from states.update_balance import UpdateBalance
from states.update_price import UpdatePrice
from utils.db_api.commands.admin import insert_txt, insert_balance_txt
from utils.db_api.commands import goods as gd
from utils.db_api.commands import photos as ph
from utils.db_api.commands import user as us
from utils.db_api.commands.balance import update_by_user
from utils.db_api.commands.user import get_all_users_mailing


@dp.message_handler(Command('login'), user_id=config.ADMINS)
async def admin_cmd(message: types.Message):
    await message.answer('Добро пожаловать в VIP-ложу этого бота.\n'
                         'Нажав на кнопки, вы сможете узнать/добавить необходимое.',
                         reply_markup=admin)


@dp.message_handler(text='Пользователи', user_id=config.ADMINS)
async def admin_users(message: types.Message):
    await message.answer('Выберите необходимую опцию на клавиатуре.',
                         reply_markup=users)


@dp.message_handler(text='Количество', user_id=config.ADMINS)
async def all_users(message: types.Message):
    counter = await us.get_all_users()
    await message.answer(f'На {datetime.date.today()}\n'
                         f'Количество пользователей составляет - {counter}',
                         reply_markup=comeback)


@dp.message_handler(text='Товары', user_id=config.ADMINS)
async def admin_goods(message: types.Message):
    await message.answer('Выберите необходимую опцию на клавиатуре',
                         reply_markup=goods)


@dp.message_handler(text='Добавить товар', user_id=config.ADMINS, state=None)
async def add_goods(message: types.Message):
    await message.answer('Чтобы добавить товар, отправьте мне следующее:\n'
                         '<b>id|категория|название|описание|дата|цена|количество|ссылка на фото (необязательно)</b>\n\n'
                         '<b>Если вы не хотите добавлять фото, то в поле "ссылка на фото" напишите None!</b>\n\n\n'
                         'Пример для заполнения:\n'
                         '1|Фрукты|Яблоки|Вкусные!|Яблоко|130|10|https://ia41.ru/wp-content/uploads/2020/09/blobid1559890085161.jpg\n'
                         '2|Steam|CS:GO PRIME|Аккаунт CS:GO с праймом. Звание в ММ - Калаш.|login:pass|200|1|None',
                         disable_web_page_preview=True)
    await Admin.first()


@dp.message_handler(state=Admin.Text)
async def state_for_goods(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=True)
    rows = message.text.split('\n')
    counter = 0
    for row in rows:
        row = row.split('|')
        await gd.insert_goods(good_id=int(row[0]), category=row[1], title=row[2], desc=row[3], data=row[4],
                              price=int(row[5]), amount=int(row[6]))
        time.sleep(3)
        photo_url = row[7]
        if IndexError:
            await ph.insert_photo(good_id=int(row[0]), photo_url=photo_url)
        else:
            pass
        counter += 1
    await message.answer('Успешно!\n'
                         f'Всего было добавлено товаров - {counter}\n'
                         f'Через 3 секунды я перенаправлю вас в админ-меню')
    time.sleep(3)
    await admin_cmd(message)


@dp.message_handler(text='Удалить товар')
async def delete_goods(message: types.Message):
    await insert_txt()
    async with aiofiles.open('goods.txt', mode='rb') as f:
        await bot.send_document(message.chat.id, f, caption='Введите ID товара для удаления')
        f.close()
    await DeleteGoods.first()


@dp.message_handler(state=DeleteGoods.Text)
async def delete_second(message: types.Message, state: FSMContext):
    await state.reset_state()
    rows = message.text.split('\n')
    counter = 0
    for row in rows:
        await gd.delete_goods_id(row)
        counter += 1
    await bot.send_message(message.chat.id, 'Товары успешно удалены.\n'
                                            f'Всего удалено - {counter} товаров\n\n'
                                            f'Через 3 секунды я перенаправлю вас в админ-меню')
    time.sleep(3)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await admin_cmd(message)


@dp.message_handler(text='Изменить цену товара')
async def edit_price(message: types.Message):
    await UpdatePrice.first()
    await insert_txt()
    async with aiofiles.open('goods.txt', mode='rb') as f:
        await bot.send_document(message.chat.id, f,
                                caption='Введите ID товара и новую цену для чего <b>ЧЕРЕЗ</b> пробел')
        f.close()


@dp.message_handler(state=UpdatePrice.Text)
async def second_edit_price(message: types.Message, state: FSMContext):
    await state.reset_state()
    rows = message.text.split('\n')
    counter = 0
    for row in rows:
        row = row.split(' ')
        await gd.update_price(int(row[0]), int(row[1]))
        counter += 1
    await message.answer(f'Отлично! Цена обновлена в {counter} товарах.')


@dp.message_handler(text='Обновить баланс')
async def update_balance(message: types.Message):
    await insert_balance_txt()
    async with aiofiles.open('users.txt', mode='rb') as f:
        await bot.send_document(message.chat.id, f, caption='Введите TelegramID и Баланс пользователя')
        f.close()
        await UpdateBalance.first()


@dp.message_handler(state=UpdateBalance.Text)
async def update_next(message: types.Message, state: FSMContext):
    global row
    await state.reset_state()
    rows = message.text.split('\n')
    for row in rows:
        row = row.split(' ')
        await update_by_user(int(row[0]), int(row[1]))
        time.sleep(2)
        await message.answer(f'Баланс пользователя с ID {row[0]} успешно пополнен на {row[1]} RUB')


@dp.message_handler(text='Рассылка', user_id=config.ADMINS)
async def mailing_handler(message: types.Message):
    await message.answer('Выберите метод рассылки', reply_markup=mailing_keyboard)


@dp.message_handler(text='Сообщение', user_id=config.ADMINS)
async def mailing_message(message: types.Message):
    await message.answer('Хорошо, пришлите мне сообщение для рассылки')
    await Mailing.first()


@dp.message_handler(state=Mailing.Text)
async def mailing_message_state(message: types.Message, state: FSMContext):
    global blocked, counter
    await state.reset_state()
    text = message.text
    rows = await get_all_users_mailing()
    try:
        counter = 0
        blocked = 0
        for row in rows:
            await bot.send_message(row, text)
            counter += 1
    except BotBlocked:
        blocked += 1

    await message.answer(f'Сообщение было доставлено - {counter} пользователям.\n'
                         f'Сообщение не получили - {blocked} пользовалей')


@dp.message_handler(text='Сообщение с картинкой', content_types=['photo', 'text'])
async def mailing_photo(message: types.Message, state: FSMContext):
    await message.answer('Хорошо, отправь мне фото, чтобы получить его ID, затем отправь мне такой шаблон:\n\n'
                         'File_ID\n'
                         'text',
                         reply_markup=comeback)
    await Mailing.Picture_get.set()


@dp.message_handler(state=Mailing.Picture_get, content_types=[types.ContentType.PHOTO, types.ContentType.ANIMATION])
async def mailing_photo_state(message: types.Message):
    try:
        await message.answer(message.photo[-1].file_id)
    except IndexError:
        await message.answer(message.animation.file_id)
    await Mailing.Picture_send.set()


@dp.message_handler(state=Mailing.Picture_send)
async def mailing_photo_send(message: types.Message, state: FSMContext):
    await state.reset_state()
    text = message.text.split('\n')
    rows = await get_all_users_mailing()
    counter = 0
    blocked = 0
    try:
        for row in rows:
            try:
                await bot.send_photo(
                    chat_id=row,
                    photo=text[0],
                    caption=text[1]
                )
                counter += 1
            except TypeOfFileMismatch:
                await bot.send_animation(
                    chat_id=row,
                    animation=text[0],
                    caption=text[1]
                )
                counter += 1
    except BotBlocked:
        blocked += 1
    await message.answer(f'Сообщение было доставлено - {counter} пользователям.\n'
                         f'Сообщение не получили - {blocked} пользовалей', reply_markup=comeback)


@dp.message_handler(text='Голосовое сообщение')
async def mailing_voice_get(message: types.Message):
    await message.answer('Отправь мне голосовое сообщение')
    await Mailing.Voice_get.set()


@dp.message_handler(state=Mailing.Voice_get, content_types=types.ContentType.VOICE)
async def mailing_voice_send(message: types.Message, state: FSMContext):
    await state.reset_state()
    voice_id = message.voice.file_id
    rows = await get_all_users_mailing()
    counter = 0
    blocked = 0
    try:
        for row in rows:
            await bot.send_voice(
                chat_id=row,
                voice=voice_id
            )
            counter += 1
    except BotBlocked:
        blocked += 1

    await message.answer(f'Сообщение было доставлено - {counter} пользователям.\n'
                         f'Сообщение не получили - {blocked} пользовалей')


@dp.message_handler(text='Видео "кружочек"')
async def mailing_video_get(message: types.Message):
    await message.answer('Отправьте мне кружочек!', reply_markup=comeback)
    await Mailing.Video_get.set()


@dp.message_handler(state=Mailing.Video_get, content_types=types.ContentType.VIDEO_NOTE)
async def mailing_video_get(message: types.Message, state: FSMContext):
    await state.reset_state()
    note_id = message.video_note.file_id
    rows = await get_all_users_mailing()
    counter = 0
    blocked = 0
    try:
        for row in rows:
            await bot.send_video_note(row, note_id)
            counter += 1
    except BotBlocked:
        blocked += 1
    await message.answer(f'Сообщение было доставлено - {counter} пользователям.\n'
                         f'Сообщение не получили - {blocked} пользовалей', reply_markup=comeback)


@dp.message_handler(text='Вернуться в меню', user_id=config.ADMINS)
async def in_menu(message: types.Message):
    await menu_cmd(message)


@dp.message_handler(text='Назад', user_id=config.ADMINS)
async def go_back(message: types.Message):
    await admin_cmd(message)
