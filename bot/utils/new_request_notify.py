from bot.data.config import ADMINS
from aiogram import Dispatcher
import logging


async def on_new_request_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Yangi ariza qabul qilindi, tekshirib ko'rishingiz mumkin")

        except Exception as err:
            logging.exception(err)