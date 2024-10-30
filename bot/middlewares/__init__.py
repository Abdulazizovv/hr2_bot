from aiogram import Dispatcher

from bot.loader import dp
from .throttling import ThrottlingMiddleware
from .translation import LanguageMiddleware



def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(LanguageMiddleware())


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(LanguageMiddleware())

