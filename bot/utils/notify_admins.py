import logging

from aiogram import Dispatcher



async def on_startup_notify(dp: Dispatcher):
    from bot.data import ADMINS
    for admin in ADMINS:
        try:
            print(admin)
            await dp.bot.send_message(admin, "Bot ishga tushdi")

        except Exception as err:
            logging.exception(err)
