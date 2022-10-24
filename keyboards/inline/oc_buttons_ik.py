from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


operation_sys = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="IOS", callback_data="ios_set_lang"),
        InlineKeyboardButton(text="Mac OS", callback_data="mac_set_lang")
    ],
    [
        InlineKeyboardButton(text="Android", callback_data="android_set_lang"),
        InlineKeyboardButton(text="Windows", callback_data="windows_set_lang"),
    ],
    [
        InlineKeyboardButton(text='В главное меню', callback_data='main_menu')
    ]
])
