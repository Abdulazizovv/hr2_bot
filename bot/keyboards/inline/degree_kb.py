from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.utils.translation import gettext as _


def degree_btn():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text=_("0 %"), callback_data="degree:0"))
    kb.add(InlineKeyboardButton(text=_("25 %"), callback_data="degree:25"))
    kb.add(InlineKeyboardButton(text=_("50 %"), callback_data="degree:50"))
    kb.add(InlineKeyboardButton(text=_("75 %"), callback_data="degree:75"))
    kb.add(InlineKeyboardButton(text=_("100 %"), callback_data="degree:100"))
    return kb