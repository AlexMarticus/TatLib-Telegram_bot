from aiogram.dispatcher.filters.state import StatesGroup, State


class Join(StatesGroup):
    email_login = State()
    password_hashed = State()
