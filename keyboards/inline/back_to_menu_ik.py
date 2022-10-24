from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

back_to_main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Вернуться в главное меню", callback_data="tat_lang_set_menu"),
    ],
])
