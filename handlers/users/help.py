from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from keyboards.default.cmd_help import cmd_help
from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer('👨‍🔧 В чём-то сомниваешься? Нужна помощь?\n'
                         'Возможно, кнопки внизу помогут тебе!', reply_markup=cmd_help)
