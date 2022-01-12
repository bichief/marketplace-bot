import logging

from aiogram import Dispatcher

from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "👨‍🔧 Бот работать за рис. Бот любить хозяин!")

        except Exception as err:
            logging.exception(err)
