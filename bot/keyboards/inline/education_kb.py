from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.utils.translation import activate, gettext as _


education_levels = ["O'rta maxsus", "O'rta", "Oliy/Bakalavr", "Oliy/Magistr"]
education_levels_ru = ["Ўрта махсус", "Ўрта", "Олий/Бакалавр", "Олий/Магистр"]

def education_levels_btn():
    kb = InlineKeyboardMarkup(row_width=1)
    for index, education_level in enumerate(education_levels):
        kb.add(InlineKeyboardButton(text=education_level, callback_data=f"education_level:{index}"))
    return kb


def education_levels_btn_ru():
    kb = InlineKeyboardMarkup(row_width=1)
    for index, education_level in enumerate(education_levels):
        kb.add(InlineKeyboardButton(text=education_level, callback_data=f"education_level:{index}"))
    return kb