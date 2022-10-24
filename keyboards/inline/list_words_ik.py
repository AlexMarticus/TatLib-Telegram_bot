from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_func import get_id_date_lvl_of_words_of_user, get_info_of_word

menu_list_words = CallbackData('list_words', 'level', 'reference_point_tracks', 'word_id', 'user_id', 'word_level')


def make_callback_data(level, reference_point_tracks=0, word_id=0, user_id=0, word_level=0):
    return menu_list_words.new(level=level, reference_point_tracks=reference_point_tracks, word_id=word_id,
                               user_id=user_id, word_level=word_level)


async def all_user_words(user_id, reference_point_tracks):
    # CURRENT_LEVEL = 1
    all_id_words_of_user = await get_id_date_lvl_of_words_of_user(user_id)
    markup = InlineKeyboardMarkup(row_width=1)
    if reference_point_tracks + 10 >= len(all_id_words_of_user):
        before = len(all_id_words_of_user)
    else:
        before = reference_point_tracks + 10
    for i in range(reference_point_tracks, before):
        word_level = all_id_words_of_user[i][2]
        word_info = await get_info_of_word(word_id=all_id_words_of_user[i][1])
        button_text = f"""{word_info[1]} — {word_info[2]}  (ур. {word_level})"""
        callback_data = make_callback_data(level=2, user_id=user_id, word_id=all_id_words_of_user[i][1],
                                           reference_point_tracks=reference_point_tracks, word_level=word_level)
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    if reference_point_tracks + 10 < len(all_id_words_of_user) and reference_point_tracks < 10:
        markup.row(
            InlineKeyboardButton(
                text="Ещё слова",
                callback_data=make_callback_data(level=1, user_id=user_id,
                                                 reference_point_tracks=(reference_point_tracks + 10)))
        )
        markup.insert(
            InlineKeyboardButton(
                text="В главное меню",
                callback_data='main_menu')
        )
    elif reference_point_tracks >= 10 and reference_point_tracks + 10 < len(all_id_words_of_user):
        markup.row(
            InlineKeyboardButton(
                text="Ещё треки",
                callback_data=make_callback_data(level=1, user_id=user_id,
                                                 reference_point_tracks=reference_point_tracks + 10))
        )
        markup.row(
            InlineKeyboardButton(
                text="Назад",
                callback_data=make_callback_data(level=1, user_id=user_id,
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
                callback_data=make_callback_data(level=1, user_id=user_id,
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


async def one_user_word_(word_id, reference_point_tracks, user_id):
    # CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Удалить",
                callback_data=make_callback_data(level=3, user_id=user_id, word_id=word_id,
                                                 reference_point_tracks=reference_point_tracks))
        ],
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data=make_callback_data(level=1, user_id=user_id,
                                                 reference_point_tracks=reference_point_tracks))
        ]
    ])
    return markup
