import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_func import get_info_of_word, get_id_date_lvl_of_words_of_user, change_lvl_of_word

menu_words_for_training = CallbackData('show_menu', 'level', 'word_id', 'reference_point_tracks', 'word_ru',
                                       'word_tat', 'word_level', 'user_id')


def make_callback_data(level, word_id='0', reference_point_tracks='0', word_ru='0', word_tat='0', word_level='0',
                       user_id='0'):
    return menu_words_for_training.new(level=level, word_id=word_id, reference_point_tracks=reference_point_tracks,
                                       word_ru=word_ru, word_tat=word_tat, word_level=word_level, user_id=user_id)


async def all_words_for_training(user_id, reference_point_tracks):
    # CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=2)
    all_words_of_user = await get_id_date_lvl_of_words_of_user(user_id)
    id_words_for_training = []
    for word in all_words_of_user:
        if word[3] <= datetime.date.today():
            if word[3] < datetime.date.today():
                await change_lvl_of_word(word_id=word[1], word_lvl=0, user_id=user_id)
            id_words_for_training.append((word[1], word[2]))
    if reference_point_tracks + 10 >= len(id_words_for_training):
        before = len(id_words_for_training)
    else:
        before = reference_point_tracks + 10
    for i in range(reference_point_tracks, before):
        word_level = id_words_for_training[i][1]
        word_id = id_words_for_training[i][0]
        word_info = await get_info_of_word(word_id)
        button_text = f"Слово №{i + 1}"
        callback_data = make_callback_data(level=1, word_id=word_id, word_tat=word_info[1], word_ru=word_info[2],
                                           reference_point_tracks=reference_point_tracks, user_id=user_id,
                                           word_level=word_level)
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    if reference_point_tracks + 10 < len(id_words_for_training) and reference_point_tracks < 10:
        markup.row(
            InlineKeyboardButton(
                text="Ещё слова",
                callback_data=make_callback_data(level=0, user_id=user_id,
                                                 reference_point_tracks=reference_point_tracks + 10))
        )
        markup.insert(
            InlineKeyboardButton(
                text="В главное меню",
                callback_data='main_menu')
        )
    elif reference_point_tracks >= 10 and reference_point_tracks + 10 < len(id_words_for_training):
        markup.row(
            InlineKeyboardButton(
                text="Ещё треки",
                callback_data=make_callback_data(level=0, user_id=user_id,
                                                 reference_point_tracks=reference_point_tracks + 10))
        )
        markup.row(
            InlineKeyboardButton(
                text="Назад",
                callback_data=make_callback_data(level=0, user_id=user_id,
                                                 reference_point_tracks=reference_point_tracks - 10))
        )
        markup.insert(
            InlineKeyboardButton(
                text="В главное меню",
                callback_data='main_menu')
        )
    elif reference_point_tracks >= 10:
        markup.row(
            InlineKeyboardButton(
                text="Назад",
                callback_data=make_callback_data(level=0, user_id=user_id,
                                                 reference_point_tracks=reference_point_tracks - 10))
        )
        markup.insert(
            InlineKeyboardButton(
                text="В главное меню",
                callback_data='main_menu')
        )
    else:
        markup.row(
            InlineKeyboardButton(
                text="В главное меню",
                callback_data='main_menu')
        )
    return markup


async def one_word_in_training(reference_point_tracks, user_id):
    # CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data='cancle_from_answer')
        ]
    ])
    return markup
