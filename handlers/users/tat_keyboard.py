from aiogram import types
from aiogram.types import CallbackQuery
from handlers.users.main_menu import delete_message
from keyboards.inline.back_to_menu_ik import back_to_main_menu
from keyboards.inline.oc_buttons_ik import operation_sys
from loader import dp


@dp.callback_query_handler(text="tat_lang_set_menu")
async def tat_lang_set_menu(call: types.CallbackQuery):
    await delete_message(call.message)
    await how_to_set_tat_language(call.message)


@dp.message_handler(text="🗣 Инструкция по установке татарской расскладки")
async def how_to_set_tat_language(message: types.Message):
    await message.answer('Выбери твою операционную систему', reply_markup=operation_sys)


@dp.callback_query_handler(text='ios_set_lang')
async def ios_set_lang(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_text("Для этого скачай Gboard (клавиатура для телефона от Google),"
                                 "при установке укажите татарский язык. В настройках телефона установи"
                                 "клавиатуру Gboard по умолчанию. Готово!", reply_markup=back_to_main_menu)


@dp.callback_query_handler(text='mac_set_lang')
async def mac_set_lang(call: CallbackQuery):
    await call.answer(cache_time=60)
    caption = 'Раскладка клавиатуры позволяет использовать привычный способ набора татарских символов в устройствах ' \
              'под управлением macOS:\n— для набора татарских букв: ө-ц, һ-§ (кнопка левее «1»), ә-щ, ү-ъ, ң-ж, ' \
              'җ-ь;\n— для набора букв ц, щ, ъ, ь, ж — необходимо вводить их с зажатой клавишей alt;\n' \
              '— для ввода точки используется клавиша «/», справа от «ю»; для ввода запятой — shift + «/».\n\n' \
              '1. Скачайте документ;\n2. Открой сохраненный файл, в открывшемся окне перенесите файлы Tatar и ' \
              'Tatar.icns в указанную папку;\n3. Перезагрузи устройство;\n4. В Настройках (System Preferences) ' \
              'открой раздел клавиатуры (Keyboard) — Источники ввода (Input Sources), нажми на кнопку +, в ' \
              'списке слева выбери Другие (Others), после чего справа выбери Tatar и нажми кнопку Добавить ' \
              '(Add).\n5. Клавиатура добавлена в список выбранных тобой раскладок и может быть использована.'
    await delete_message(call.message)
    await call.message.answer_document(document='BQACAgIAAxkBAAIMzWNQTHje7Kx6qVjv-1elApuaCNstAALhIAACux-BSgg'
                                                '6liyK45SBKgQ', caption=caption, reply_markup=back_to_main_menu)


@dp.callback_query_handler(text='android_set_lang')
async def android_set_lang(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_text("Для этого скачай Gboard (клавиатура для телефона от Google),"
                                 "при установке укажите татарский язык. В настройках телефона установите"
                                 "клавиатуру Gboard по умолчанию. Готово!", reply_markup=back_to_main_menu)


@dp.callback_query_handler(text='windows_set_lang')
async def windows_set_lang(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_text("""Для этого кликаем правой кнопкой мышки на «Языковую панель» («RU»), 
которая расположена в правом нижнем углу экрана. Выбираем пункт «Параметры» 
и переходим в окно «Языки и службы текстового ввода». Теперь остаётся только выбрать и добавить язык!
Расположение татарских букв (кириллица) основано на русской клавиатуре. Когда вы будете набирать текст на 
татарском языке, тебе придётся нажимать клавиши, которые используются сравнительно редко. 
По решению Microsoft татарские буквы расположены так, как показано ниже:

Буква Ә на клавише Щ;
Буква Ө на клавише Ц;
Буква Ү на клавише Ъ; 
Буква Җ на клавише Ь; 
Буква Ң на клавише Ж;
Буква Һ на клавише Ё.

Если в тексте тебе нужно использовать эти русские буквы, не нужно менять раскладку: их следует писать,
нажимая одновременно с клавишами «Ctrl» и «Alt». Например, чтобы набрать букву «ж», нажмите одновременно «Ctrl+Alt+ж».
""", reply_markup=back_to_main_menu)
