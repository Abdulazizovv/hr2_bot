from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.utils.translation import gettext as _


def has_car_btn():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text=_("Ha✅"), callback_data="has_car:1"))
    kb.add(InlineKeyboardButton(text=_("Yo'q❌"), callback_data="has_car:0"))
    return kb