from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_func import is_word_added_to_user
from utils.translate import translate_rus_to_tat

menu_new_words = CallbackData('new_words', 'level', 'topic_id', 'reference_point_tracks', 'word_ru', 'word_tat',
                              'user_id', 'is_added')


def make_callback_data(level, reference_point_tracks=0, word_ru='0', word_tat='0', topic_id=0, user_id=0,
                       is_added=False):
    return menu_new_words.new(level=level, reference_point_tracks=reference_point_tracks, word_ru=word_ru,
                              word_tat=word_tat, topic_id=topic_id, user_id=user_id, is_added=is_added)


async def all_topics():
    # CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)
    topics = [('Семья', 1), ('Погода', 2), ('Еда', 3), ('Путешествие', 4)]
    for i in topics:
        topic_id = i[1]
        topic_name = i[0]
        button_text = topic_name
        callback_data = make_callback_data(level=2, topic_id=topic_id)
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(InlineKeyboardButton(text='Вернуться в меню', callback_data="main_menu"))
    return markup


async def one_topic_(topic_id, reference_point_tracks, user_id):
    # CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=2)
    if topic_id == 1:
        all_words = ["отец", "мать", "родители", "сын", "дочь", "сестра", "брат", "двоюродный брат", "родной брат",
                     "троюродный брат", "сестра", "близнецы", "тетя", "дядя", "племянник", "племянница", "дедушка",
                     "бабушка", "дедушка и бабушка", "прабабушка", "прадедушка", "внук", "внучка", "муж", "жена",
                     "ребенок", "дети", "внуки", "малыш", "родственник"]
    elif topic_id == 2:
        all_words = ["погода", "прекрасный", "ужасный", "холодный", "жаркий", "теплый", "небо", "солнце", "дождь",
                     "ветер", "облако", "снег", "солнечный", "дождливый", "ветреный", "облачный", "яркий", "снежный",
                     "идет", "дождь", "идет", "снег", "дуть", "светить", "теплее", "становиться", "холоднее",
                     "измениться"]
    elif topic_id == 3:
        all_words = ["бутерброд", "поджаренный хлеб", "торт, пирожное", "булочка", "чай", "кофе", "сахар", "каша",
                     "сыр", "колбаса", "сосиски", "соль", "перец", "салат", "суп", "мясо", "курица", "рыба", "котлеты",
                     "картошка", "помидоры", "овощи", "суп", "хлеб", "масло", "напиток", "молоко", "сок", "кока-кола",
                     "минеральная вода", "мороженое", "фрукты", " завтрак", " обед", "ужин", "выпить кофе вместо чая",
                     "испытывать голод", "испытывать жажду", "пить", "есть", "готовить", "налить чашечку чая",
                     "мыть посуду", "мыть руки перед едой", " быть готовым", "закончен"]
    elif topic_id == 4:
        all_words = ['комната', 'номер', 'помещение', 'место', 'оставлять', 'отпуск', 'покидать', 'уходить', 'уезжать',
                     'деревня', 'село', 'городок', 'побережье', 'берег', 'береговой', 'сезон', 'время года', 'период',
                     'время', 'сезонный', 'сиденье', 'место', 'местонахождение', 'сидеть', 'вмещать', 'путешествие',
                     'поездка', 'рейс', 'полет', 'перелет', 'бегство', 'пляж', 'ворота', 'затвор', 'калитка', 'шлюз',
                     'прибытие', 'приход', 'приезд', 'ресторан']
    else:
        all_words = ['Пусто']
    if reference_point_tracks + 10 >= len(all_words):
        before = len(all_words)
    else:
        before = reference_point_tracks + 10
    for i in range(reference_point_tracks, before):
        is_added = await is_word_added_to_user(word_ru=all_words[i], user_id=user_id)
        if is_added:
            button_text = f"{all_words[i][0].upper() + all_words[i][1:]} (доб.)"
        else:
            button_text = all_words[i][0].upper() + all_words[i][1:]
        callback_data = make_callback_data(level=3, word_ru=all_words[i],
                                           reference_point_tracks=reference_point_tracks, user_id=user_id,
                                           is_added=is_added, topic_id=topic_id)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    if reference_point_tracks + 10 < len(all_words) and reference_point_tracks < 10:
        markup.row(
            InlineKeyboardButton(
                text="Ещё слова",
                callback_data=make_callback_data(level=2, topic_id=topic_id, user_id=user_id,
                                                 reference_point_tracks=reference_point_tracks + 10))
        )
        markup.row(
            InlineKeyboardButton(
                text="К темам",
                callback_data=make_callback_data(level=1))
        )
    elif reference_point_tracks >= 10 and reference_point_tracks + 10 < len(all_words):
        markup.row(
            InlineKeyboardButton(
                text="Ещё слова",
                callback_data=make_callback_data(level=2, topic_id=topic_id, user_id=user_id,
                                                 reference_point_tracks=reference_point_tracks + 10))
        )
        markup.row(
            InlineKeyboardButton(
                text="Назад",
                callback_data=make_callback_data(level=2, topic_id=topic_id, user_id=user_id,
                                                 reference_point_tracks=reference_point_tracks - 10))
        )
        markup.insert(
            InlineKeyboardButton(
                text="К темам",
                callback_data=make_callback_data(level=1))
        )
    elif reference_point_tracks >= 10:
        markup.row(
            InlineKeyboardButton(
                text="Назад",
                callback_data=make_callback_data(level=2, topic_id=topic_id, user_id=user_id,
                                                 reference_point_tracks=reference_point_tracks - 10))
        )
        markup.row(
            InlineKeyboardButton(
                text="К темам",
                callback_data=make_callback_data(level=1))
        )
    else:
        markup.row(
            InlineKeyboardButton(
                text="К темам",
                callback_data=make_callback_data(level=1))
        )
    return markup


async def one_word_(topic_id, reference_point_tracks, word_ru, word_tat, user_id, is_added):
    # CURRENT_LEVEL = 3
    if is_added != 'False':
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=make_callback_data(level=2, topic_id=topic_id, user_id=user_id,
                                                     reference_point_tracks=reference_point_tracks))
            ]
        ])
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Выучить",
                    callback_data=make_callback_data(level=4, user_id=user_id, topic_id=topic_id,
                                                     reference_point_tracks=reference_point_tracks, word_ru=word_ru,
                                                     word_tat=word_tat))
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=make_callback_data(level=2, topic_id=topic_id, user_id=user_id,
                                                     reference_point_tracks=reference_point_tracks))
            ]
        ])
    return markup
