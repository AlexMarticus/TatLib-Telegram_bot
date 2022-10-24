import asyncio
from contextlib import suppress

from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
from keyboards.default.start_dk import start_menu
from loader import dp


@dp.callback_query_handler(text="main_menu")
async def main_menu(call: types.CallbackQuery):
    await delete_message(call.message)
    await call.message.answer('Вернули в главное меню', reply_markup=start_menu)


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()
