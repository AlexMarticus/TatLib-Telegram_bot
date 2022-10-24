import datetime
import psycopg
from data.config import PG_USER, DB_NAME, PG_PASS, PG_HOST


async def is_word_in_db(word_ru):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} "
                                                     f"password={PG_PASS} host={PG_HOST}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT word_tat FROM words WHERE word_ru = %s", (word_ru,))
            try:
                return (await acur.fetchone())[0]
            except TypeError:
                return False


async def delete_message_db(user_id, word_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} "
                                                     f"password={PG_PASS} host={PG_HOST}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute('''DELETE FROM users_to_words WHERE (user_id = %s AND word_id = %s)''', (user_id,
                                                                                                        word_id))
            await aconn.commit()


async def add_word_to_user(word_id, user_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} "
                                                     f"password={PG_PASS} host={PG_HOST}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute('INSERT INTO users_to_words (word_id, user_id, next_date_training) '
                               'VALUES (%s, %s, %s)', (word_id, user_id, datetime.date.today()))
            await aconn.commit()


async def add_word(word_ru, word_tat):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} "
                                                     f"password={PG_PASS} host={PG_HOST}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute('INSERT INTO words (word_ru, word_tat) '
                               'VALUES (%s, %s)', (word_ru, word_tat))
            await aconn.commit()


async def change_lvl_of_word(word_id, word_lvl, user_id, date=datetime.date.today()):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} "
                                                     f"password={PG_PASS} host={PG_HOST}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("UPDATE users_to_words SET word_level = %s WHERE (word_id = %s AND user_id = %s)",
                               (word_lvl, word_id, user_id))
            await aconn.commit()
            await acur.execute("UPDATE users_to_words SET next_date_training = %s WHERE "
                               "(word_id = %s AND user_id = %s)", (date, word_id, user_id))
            await aconn.commit()


async def get_info_of_word(word_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} "
                                                     f"password={PG_PASS} host={PG_HOST}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT * FROM words WHERE id = %s", (word_id,))
            return await acur.fetchone()


async def get_id_date_lvl_of_words_of_user(user_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} "
                                                     f"password={PG_PASS} host={PG_HOST}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT * FROM users_to_words WHERE user_id = %s", (user_id,))
            return await acur.fetchall()


async def is_word_added_to_user(word_ru, user_id=0, id_only=False):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} "
                                                     f"password={PG_PASS} host={PG_HOST}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT id FROM words WHERE word_ru = %s", (word_ru,))
            try:
                word_id = (await acur.fetchone())[0]
            except TypeError:
                return False
            if id_only:
                return word_id
            await acur.execute("SELECT count(user_id) FROM users_to_words WHERE (word_id = %s AND user_id = %s)",
                               (word_id, user_id))
            if (await acur.fetchone())[0] == 0:
                return False
            return True


async def get_id_lvl_of_words_of_user_this_day_and_later(user_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} "
                                                     f"password={PG_PASS} host={PG_HOST}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT * FROM users_to_words WHERE (user_id = %s AND next_date_training <= %s)",
                               (user_id, datetime.date.today()))
            return await acur.fetchall()


async def check_is_new_user(tg_id=None, tg_username=None):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} "
                                                     f"password={PG_PASS} host={PG_HOST}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT count(id) FROM users WHERE tg_id = %s", (tg_id,))
            count = (await acur.fetchone())[0]
            if count == 0:
                await acur.execute("SELECT count(id) FROM users WHERE tg_username = %s", (tg_username,))
                count = (await acur.fetchone())[0]
                if count == 0:
                    return False
                await acur.execute("UPDATE users SET tg_id = %s WHERE tg_username = %s", (tg_id, tg_username,))
                await aconn.commit()
                return True
            return True


async def is_true_login_or_email(email_login):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} "
                                                     f"password={PG_PASS} host={PG_HOST}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT count(id) FROM users WHERE login = %s", (email_login,))
            login = (await acur.fetchone())[0]
            if login == 0:
                await acur.execute("SELECT count(id) FROM users WHERE email = %s", (email_login,))
                email = (await acur.fetchone())[0]
                if email == 0:
                    return False
                return True
            return True


async def get_hashed_password(user_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} "
                                                     f"password={PG_PASS} host={PG_HOST}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT hashed_password FROM users WHERE id = %s", (user_id,))
            return (await acur.fetchone())[0]


async def get_user_id_from_email_or_login_or_tg_id(email_login=None, tg_id=None):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} "
                                                     f"password={PG_PASS} host={PG_HOST}") as aconn:
        async with aconn.cursor() as acur:
            try:
                await acur.execute("SELECT id FROM users WHERE tg_id = %s", (tg_id,))
                return (await acur.fetchone())[0]
            except TypeError:
                await acur.execute("SELECT id FROM users WHERE login = %s", (email_login,))
                try:
                    return (await acur.fetchone())[0]
                except TypeError:
                    await acur.execute("SELECT id FROM users WHERE email = %s", (email_login,))
                    return (await acur.fetchone())[0]


async def add_tg_info_when_he_joined(user_id, tg_id, tg_username):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} "
                                                     f"password={PG_PASS} host={PG_HOST}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("UPDATE users SET tg_id = %s WHERE id = %s", (tg_id, user_id,))
            await aconn.commit()
            await acur.execute("UPDATE users SET tg_username = %s WHERE id = %s", (tg_username, user_id,))
            await aconn.commit()


async def is_email_uniq(email):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} "
                                                     f"password={PG_PASS} host={PG_HOST}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT count(id) FROM users WHERE email = %s", (email,))
            count = (await acur.fetchone())[0]
            if count == 0:
                return True
            return False


async def is_login_uniq(login):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} "
                                                     f"password={PG_PASS} host={PG_HOST}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT count(id) FROM users WHERE login = %s", (login,))
            count = (await acur.fetchone())[0]
            if count == 0:
                return True
            return False


async def create_user(email, login, hashed_password, tg_id, tg_username):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} "
                                                     f"password={PG_PASS} host={PG_HOST}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute('''INSERT INTO users (login, email, tg_username, tg_id, hashed_password, creation_date) 
VALUES (%s, %s, %s, %s, %s, %s)''',
                               (login, email, tg_username, tg_id, hashed_password, datetime.date.today()))
            await aconn.commit()
