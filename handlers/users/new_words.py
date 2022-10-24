from typing import Union
from aiogram import types
from handlers.users.main_menu import delete_message
from keyboards.inline.new_words_ik import all_topics, menu_new_words, one_topic_, one_word_
from loader import dp
from utils.db_func import get_user_id_from_email_or_login_or_tg_id, is_word_added_to_user, add_word, add_word_to_user, \
    is_word_in_db
from utils.translate import translate_rus_to_tat


@dp.message_handler(text="🧠 Выучить новые слова")
async def new_words_themes(message: types.Message):
    await list_topics(message)


async def list_topics(message: Union[types.CallbackQuery, types.Message], **kwargs):
    if isinstance(message, types.Message):
        message1 = await message.answer(text='📤 Загрузка')
    elif isinstance(message, types.CallbackQuery):
        await message.message.edit_text(text='📤 Загрузка')
    markup = await all_topics()
    if isinstance(message, types.Message):
        await delete_message(message1)
        await message.answer(text='Выбери нужную тебе тему', reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        await message.message.edit_text(text='Выбери нужную тебе тему', reply_markup=markup)


async def one_topic(call: types.CallbackQuery, topic_id, reference_point_tracks=0, **kwargs):
    await call.message.edit_text('📤 Загрузка')
    user_id = await get_user_id_from_email_or_login_or_tg_id(tg_id=call.from_user.id)
    markup = await one_topic_(topic_id=topic_id, reference_point_tracks=reference_point_tracks, user_id=user_id)
    await call.message.edit_text('Выбери нужное тебе слово', reply_markup=markup)


async def one_word(call: types.CallbackQuery, topic_id, reference_point_tracks, word_ru, user_id, is_added,
                   **kwargs):
    await call.message.edit_text('📤 Загрузка')
    word_tat = await is_word_in_db(word_ru)
    if word_tat is False:
        word_tat = translate_rus_to_tat(word_ru)
        await add_word(word_ru=word_ru, word_tat=word_tat)
    markup = await one_word_(topic_id=topic_id, reference_point_tracks=reference_point_tracks, word_ru=word_ru,
                             word_tat=word_tat, user_id=user_id, is_added=is_added)
    if is_added != 'False':
        await call.message.edit_text(f'{word_ru} — {word_tat} (уже изучается)', reply_markup=markup)
    else:
        await call.message.edit_text(f'{word_ru} — {word_tat}', reply_markup=markup)


async def learn_word(call: types.CallbackQuery, user_id, topic_id, word_ru, word_tat, reference_point_tracks, **kwargs):
    word_id = await is_word_added_to_user(id_only=True, word_ru=word_ru)
    if not word_id:
        await add_word(word_ru=word_ru, word_tat=word_tat)
        word_id = await is_word_added_to_user(id_only=True, word_ru=word_ru)
    await add_word_to_user(word_id=word_id, user_id=user_id)
    markup = await one_topic_(topic_id=topic_id, reference_point_tracks=reference_point_tracks, user_id=user_id)
    await call.message.edit_text(f'Слово {word_ru} добавлено в систему изучения', reply_markup=markup)


@dp.callback_query_handler(menu_new_words.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict, state=None):
    current_level = callback_data.get("level")
    topic_id = int(callback_data.get("topic_id"))
    user_id = int(callback_data.get("user_id"))
    word_ru = callback_data.get("word_ru")
    reference_point_tracks = int(callback_data.get("reference_point_tracks"))
    word_tat = callback_data.get("word_tat")
    is_added = callback_data.get("is_added")
    levels = {
        "1": list_topics,
        "2": one_topic,
        "3": one_word,
        "4": learn_word
    }
    current_level_function = levels[current_level]
    await current_level_function(
        call,
        lvl=current_level,
        topic_id=topic_id,
        word_ru=word_ru,
        state=state,
        reference_point_tracks=reference_point_tracks,
        word_tat=word_tat,
        user_id=user_id,
        is_added=is_added
    )
