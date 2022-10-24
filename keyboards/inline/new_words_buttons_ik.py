from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

themes_for_new_words = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Погода", callback_data="whether_kb"),
        InlineKeyboardButton(text="Семья", callback_data="family_kb")
    ],
    [
        InlineKeyboardButton(text="Еда", callback_data="food_kb"),
        InlineKeyboardButton(text="Путешествие", callback_data="travelling_kb"),
    ]
])
