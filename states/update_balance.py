from aiogram.dispatcher.filters.state import StatesGroup, State


class UpdateBalance(StatesGroup):
    Text = State()