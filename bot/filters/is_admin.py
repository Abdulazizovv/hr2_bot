from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from bot.data import config
from asgiref.sync import sync_to_async
from bot.utils.db_api import get_bot_admins_id

@sync_to_async
def bot_admins():
    return list(get_bot_admins_id())


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        
        if str(message.from_user.id) in config.ADMINS or str(message.from_user.id) in await bot_admins():
            return True
