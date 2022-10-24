from aiogram import types
from aiogram.dispatcher import FSMContext
from handlers.users.main_menu import delete_message
from handlers.users.start import bot_start
from keyboards.default.start_dk import start_menu
from loader import dp
from states.registration_state import Registration
from utils.db_func import is_email_uniq, is_login_uniq, create_user
from werkzeug.security import generate_password_hash


async def hash_password(unhashed_password):
    return generate_password_hash(unhashed_password)


@dp.message_handler(text="👤 Регистрация")
async def reg(message: types.Message):
    await message.answer('Введи свою почту', reply_markup=types.ReplyKeyboardRemove())
    await Registration.email.set()


@dp.message_handler(state=Registration.email)
async def reg_email(message: types.Message, state: FSMContext):
    if '@' in message.text and (await is_email_uniq(message.text)):
        await state.update_data(email=message.text)
        await message.answer('Придумай логин')
        await Registration.login.set()
    elif not(await is_email_uniq(message.text)):
        await message.answer("Такая почта уже зарегистрирована")
        await Registration.email.set()
    else:
        await message.answer("Неверный формат ввода")
        await Registration.email.set()


@dp.message_handler(state=Registration.login)
async def reg_login(message: types.Message, state: FSMContext):
    if await is_login_uniq(message.text):
        await state.update_data(login=message.text)
        await message.answer('Придумай пароль (твоё сообщение будет автоматически удалено в целях безопасности)')
        await Registration.password_hashed.set()
    else:
        await message.answer("Такой логин уже занят")
        await Registration.login.set()


@dp.message_handler(state=Registration.password_hashed)
async def reg_passw(message: types.Message, state: FSMContext):
    await state.update_data(hashed_password=await hash_password(message.text))
    await delete_message(message)
    cc = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text='Всё верно', callback_data='reg_yes')],
            [types.InlineKeyboardButton(text='Ввести заново', callback_data='reg_change'),
             types.InlineKeyboardButton(text='Отмена', callback_data='reg_back')]
        ]
    )
    data = await state.get_data()
    await message.answer(f"""Проверь данные:
Почта: {data.get('email')}
Логин: {data.get('login')}

Всё верно?""", reply_markup=cc)
    await Registration.confirm.set()


@dp.callback_query_handler(text='reg_back', state=Registration.confirm)
async def ch_change(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=False)
    message = call.message
    await delete_message(call.message)
    await bot_start(call.message)


@dp.callback_query_handler(text='reg_change', state=Registration.confirm)
async def ch_change(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.edit_text('Введи заново Вашу почту')
    await Registration.email.set()


@dp.callback_query_handler(text='reg_yes', state=Registration.confirm)
async def ch_yes(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    await create_user(email=data.get('email'), login=data.get('login'), hashed_password=data.get('hashed_password'),
                      tg_id=call.from_user.id, tg_username=call.from_user.username)
    await delete_message(call.message)
    await call.message.answer('🫰 Ты успешно прошёл регистрацию', reply_markup=start_menu)
    await state.reset_state(with_data=False)
