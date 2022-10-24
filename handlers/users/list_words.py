from typing import Union

from aiogram import types

from handlers.users.main_menu import delete_message
from keyboards.inline.list_words_ik import all_user_words, one_user_word_, menu_list_words
from loader import dp
from utils.db_func import get_user_id_from_email_or_login_or_tg_id, get_info_of_word, delete_message_db


@dp.message_handler(text="📑 Список изучаемых слов")
async def new_words_themes(message: types.Message):
    await list_user_words(message)


async def list_user_words(message: Union[types.CallbackQuery, types.Message],
                          reference_point_tracks=0, **kwargs):
    if isinstance(message, types.Message):
        message1 = await message.answer(text='📤 Загрузка')
    elif isinstance(message, types.CallbackQuery):
        await message.message.edit_text(text='📤 Загрузка')
    user_id = await get_user_id_from_email_or_login_or_tg_id(tg_id=message.from_user.id)
    markup = await all_user_words(user_id, reference_point_tracks=reference_point_tracks)
    if markup['inline_keyboard'][0][0]['callback_data'] == 'main_menu':
        text = 'Твой список слов пока пуст'
    else:
        text = 'Выбери нужное слово'
    if isinstance(message, types.Message):
        await delete_message(message1)
        await message.answer(text=text, reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        await message.message.edit_text(text=text, reply_markup=markup)


async def one_user_word(call: types.CallbackQuery, word_id, reference_point_tracks, user_id, word_level, **kwargs):
    markup = await one_user_word_(word_id=word_id, reference_point_tracks=reference_point_tracks, user_id=user_id)
    word_info = await get_info_of_word(word_id=word_id)
    text = f"""Татар: {word_info[1]}
Рус: {word_info[2]}
Уровень: {word_level}
"""
    await call.message.edit_text(text=text, reply_markup=markup)


async def delete_word(call: types.CallbackQuery, word_id, reference_point_tracks, user_id, **kwargs):
    await call.message.edit_text(text='📤 Загрузка')
    await delete_message_db(user_id=user_id, word_id=word_id)
    markup = await all_user_words(user_id=user_id, reference_point_tracks=reference_point_tracks)
    text = 'Слово удалено'
    await call.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query_handler(menu_list_words.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict, state=None):
    current_level = callback_data.get("level")
    user_id = int(callback_data.get("user_id"))
    reference_point_tracks = int(callback_data.get("reference_point_tracks"))
    word_id = int(callback_data.get("word_id"))
    word_level = int(callback_data.get("word_level"))
    levels = {
        "1": list_user_words,
        "2": one_user_word,
        "3": delete_word
    }
    current_level_function = levels[current_level]
    await current_level_function(
        call,
        lvl=current_level,
        state=state,
        reference_point_tracks=reference_point_tracks,
        user_id=user_id,
        word_id=word_id,
        word_level=word_level
    )
