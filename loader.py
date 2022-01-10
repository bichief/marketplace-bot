from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pyqiwip2p.AioQiwip2p import AioQiwiP2P

from data import config


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
p2p = AioQiwiP2P(auth_key=config.QIWI_KEY)