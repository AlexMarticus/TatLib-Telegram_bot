import datetime
import random
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.main_menu import delete_message
from keyboards.inline.words_training_ik import all_words_for_training, menu_words_for_training, one_word_in_training
from loader import dp
from states.translate_word_state import Translation
from utils.db_func import get_user_id_from_email_or_login_or_tg_id, change_lvl_of_word


@dp.message_handler(text="🧑‍🏫 Тренировка на день")
async def start_training(message: types.Message):
    await list_words(message)


async def list_words(message: Union[types.CallbackQuery, types.Message], reference_point_tracks=0, **kwargs):
    if isinstance(message, types.Message):
        message1 = await message.answer(text='📤 Загрузка')
    elif isinstance(message, types.CallbackQuery):
        await message.message.edit_text(text='📤 Загрузка')
    user_id = await get_user_id_from_email_or_login_or_tg_id(tg_id=message.from_user.id)
    markup = await all_words_for_training(user_id=user_id, reference_point_tracks=reference_point_tracks)
    if markup['inline_keyboard'][0][0]['callback_data'] == 'main_menu':
        text = 'Слов для изучения на сегодня нет'
    else:
        text = 'Все слова. При выборе одного из слов тебе будет предложен 1 из вариатнтов:\n-' \
               'перевести слова с татарского на русский\n-перевести слова с русского на татарский'
    if isinstance(message, types.Message):
        await delete_message(message1)
        await message.answer(text=text,
                             reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text(text=text, reply_markup=markup)


async def one_word(call: types.CallbackQuery, state: FSMContext, word_tat, word_ru, user_id,
                   reference_point_tracks, word_level, word_id, **kwargs):
    a = random.choice((word_tat, word_ru))
    if a == word_tat:
        await state.update_data(true_answer=word_ru, reference_point_tracks=reference_point_tracks, user_id=user_id,
                                word_level=word_level, word_id=word_id)
    else:
        await state.update_data(true_answer=word_tat, reference_point_tracks=reference_point_tracks, user_id=user_id,
                                word_level=word_level, word_id=word_id)
    markup = await one_word_in_training(reference_point_tracks=reference_point_tracks, user_id=user_id)
    await call.message.edit_text(f'Как переводится слово {a}?', reply_markup=markup)
    await state.update_data(reference_point_tracks=reference_point_tracks)
    await Translation.word.set()


@dp.message_handler(state=Translation.word)
async def answer(message: types.Message, state: FSMContext, **kwargs):
    answer_ = message.text.lower()
    data = await state.get_data()
    if data.get('true_answer') == answer_:
        if data.get('word_level') == '0':
            date = datetime.date.today() + datetime.timedelta(days=1)
        elif data.get('word_level') == '1':
            date = datetime.date.today() + datetime.timedelta(days=2)
        elif data.get('word_level') == '2':
            date = datetime.date.today() + datetime.timedelta(days=3)
        elif data.get('word_level') == '3':
            date = datetime.date.today() + datetime.timedelta(days=7)
        elif data.get('word_level') == '4':
            date = datetime.date.today() + datetime.timedelta(days=15)
        elif data.get('word_level') == '5':
            date = datetime.date.today() + datetime.timedelta(days=30)
        elif data.get('word_level') == '6':
            date = datetime.date.today() + datetime.timedelta(days=30)
        elif data.get('word_level') == '7':
            date = datetime.date.today() + datetime.timedelta(days=60)
        else:
            date = datetime.date.today() + datetime.timedelta(days=365)
        await change_lvl_of_word(word_id=data.get('word_id'), word_lvl=(int(data.get('word_level')) + 1), date=date,
                                 user_id=data.get('user_id'))
        markup = await all_words_for_training(user_id=data.get('user_id'),
                                              reference_point_tracks=data.get('reference_point_tracks'))
        await message.answer('Ответ верный', reply_markup=markup)
    else:
        await change_lvl_of_word(word_id=data.get('word_id'), user_id=data.get('user_id'),
                                 word_lvl=0,
                                 date=datetime.date.today())
        markup = await all_words_for_training(user_id=data.get('user_id'),
                                              reference_point_tracks=data.get('reference_point_tracks'))
        await message.answer(f'Ответ <strike>{answer_}</strike> неверный. Правильный ответ — {data.get("true_answer")}',
                             reply_markup=markup)
    await state.reset_state(with_data=False)


@dp.callback_query_handler(text='cancle_from_answer', state=Translation.word)
async def cancle_from_answer(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await list_words(call, reference_point_tracks=data.get('reference_point_tracks'))
    await state.reset_state(with_data=False)


@dp.callback_query_handler(menu_words_for_training.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict, state=None):
    current_level = callback_data.get("level")
    word_id = int(callback_data.get("word_id"))
    word_ru = callback_data.get("word_ru")
    user_id = callback_data.get("user_id")
    reference_point_tracks = int(callback_data.get("reference_point_tracks"))
    word_tat = callback_data.get("word_tat")
    word_level = callback_data.get("word_level")
    levels = {
        "0": list_words,
        "1": one_word,
    }
    current_level_function = levels[current_level]
    await current_level_function(
        call,
        lvl=current_level,
        word_id=word_id,
        word_ru=word_ru,
        state=state,
        reference_point_tracks=reference_point_tracks,
        word_tat=word_tat,
        word_level=word_level,
        user_id=user_id
    )
