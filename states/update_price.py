from aiogram.dispatcher.filters.state import StatesGroup, State


class UpdatePrice(StatesGroup):
    Text = State()