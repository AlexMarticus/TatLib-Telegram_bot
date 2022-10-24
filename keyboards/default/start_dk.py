from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_for_registrantion = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='👤 Регистрация'),
            KeyboardButton(text='📑 Вход')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🧑‍🏫 Тренировка на день'),
            KeyboardButton(text='📑 Список изучаемых слов')
        ],
        [
            KeyboardButton(text='🧠 Выучить новые слова'),
            KeyboardButton(text='📝 Тест на знание татарского')
        ],
        [
            KeyboardButton(text='🗣 Инструкция по установке татарской расскладки')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

admin_start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Рассылка')
        ],
        [
            KeyboardButton(text='Добавить слово'),
        ],
        [
            KeyboardButton(text=''),
        ],
        [
            KeyboardButton(text=''),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
