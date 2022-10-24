from aiogram import types
from aiogram.dispatcher import FSMContext
from werkzeug.security import check_password_hash
from handlers.users.main_menu import delete_message
from keyboards.default.start_dk import start_menu, menu_for_registrantion
from loader import dp
from states.join_state import Join
from states.registration_state import Registration
from utils.db_func import get_hashed_password, is_true_login_or_email, add_tg_info_when_he_joined, \
    get_user_id_from_email_or_login_or_tg_id


async def is_true_login_details(email_login, unhashed_password, tg_id):
    if check_password_hash(pwhash=(await get_hashed_password(tg_id)), password=unhashed_password) and \
            await is_true_login_or_email(email_login, tg_id):
        return True


@dp.message_handler(text="📑 Вход")
async def join(message: types.Message):
    await message.answer('Введи email или логин', reply_markup=types.ReplyKeyboardRemove())
    await Join.email_login.set()


@dp.message_handler(state=Join.email_login)
async def join_email_or_login(message: types.Message, state: FSMContext):
    if await is_true_login_or_email(message.text):
        await state.update_data(user_id=await get_user_id_from_email_or_login_or_tg_id(message.text))
        await message.answer('Введи пароль (твоё сообщение будет автоматически удалено в целях безопасности)')
        await Join.password_hashed.set()
    else:
        await message.answer('Пользователя с такими данными не существует. Можешь пройти регистрацию',
                             reply_markup=menu_for_registrantion)
        await state.reset_state(with_data=False)


@dp.message_handler(state=Join.password_hashed)
async def reg_passw(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if check_password_hash(pwhash=(await get_hashed_password(data.get('user_id'))), password=message.text):
        await delete_message(message)
        await state.reset_state(with_data=False)
        await add_tg_info_when_he_joined(tg_username=message.from_user.username, tg_id=message.from_user.id,
                                         user_id=data.get('user_id'))
        await message.answer('Вход выполнен успешно', reply_markup=start_menu)
    else:
        await delete_message(message)
        await message.answer("Неверный пароль😟", reply_markup=menu_for_registrantion)
        await Registration.login.set()
