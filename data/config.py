from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = list(map(lambda x: int(x), env.list("ADMINS")))

DB_NAME = env.str('DB_NAME')
PG_USER = env.str("PG_USER")
PG_PASS = env.str("PG_PASS")
PG_HOST = env.str("PG_HOST")