from aiogram.dispatcher.filters.state import StatesGroup, State


class Language(StatesGroup):
    set_lang = State()