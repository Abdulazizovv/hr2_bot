from environs import Env
from bot.utils.db_api.db import get_bot_admins
# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati

for new_admin in get_bot_admins():
    if new_admin not in ADMINS:
        ADMINS.append(new_admin)
CHANNEL_ID = env.str("CHANNEL_ID")  # Kanal idsi
# IP = env.str("ip")  # Xosting ip manzili
# password = env.str("PASSWORD")  # Xosting ip manzili

