import translators as ts


async def translate_tat_to_rus(word_tat):
    return ts.google(word_tat, from_language='tt', to_language='ru')


def translate_rus_to_tat(word_ru):
    return ts.google(word_ru, from_language='ru', to_language='tt')


# print(translate_rus_to_tat('путешествовать (ехать) по …'))
