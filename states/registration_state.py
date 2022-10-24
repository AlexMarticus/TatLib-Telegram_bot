from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
    email = State()
    login = State()
    password_hashed = State()
    confirm = State()
