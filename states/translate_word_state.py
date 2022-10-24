from aiogram.dispatcher.filters.state import StatesGroup, State


class Translation(StatesGroup):
    word = State()

