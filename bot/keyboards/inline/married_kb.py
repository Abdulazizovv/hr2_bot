from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.utils.translation import gettext as _


def married_btn():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text=_("Turmush qurgan"), callback_data="married:1"))
    kb.add(InlineKeyboardButton(text=_("Turmush qurmagan"), callback_data="married:0"))
    return kb