from aiogram.dispatcher.filters.state import StatesGroup, State


class Mailing(StatesGroup):
    Text = State()
    Picture_get = State()
    Picture_send = State()
    Voice_get = State()
    Video_get = State()
    Message = State()