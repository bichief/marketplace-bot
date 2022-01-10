from aiogram.dispatcher.filters.state import StatesGroup, State


class NewPayment(StatesGroup):
    amount = State()