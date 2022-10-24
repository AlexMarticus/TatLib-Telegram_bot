from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.start_dk import start_menu, menu_for_registrantion
from loader import dp
from utils.db_func import check_is_new_user


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    is_new = await check_is_new_user(tg_id=message.from_user.id, tg_username=message.from_user.username)
    if not is_new:
        await message.answer(f"👋 Привет, {message.from_user.full_name}!\nУ нас реализована экосистема сайт-telegram. "
                             f"Я не нашёл информации о тебе😔 Если ты ещё не знаком с нами, то регистрируйся, "
                             f"потому что мы поможем тебе в изучении татарского 😉\n"
                             f"Уже зарегистрирован? Ты забыл указать свой username☹ Входи в свой аккаунт "
                             f"и продолжай обучение 🤗", reply_markup=menu_for_registrantion)
    else:
        await message.answer(f"👋 Привет, {message.from_user.full_name}!\nКак настроение? "
                             f"Выбирай нужную тебе кнопку ⌨", reply_markup=start_menu)
