from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.utils.translation import gettext as _

def convince_btn():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text=_("Ha✅"), callback_data="convince:1"))
    kb.add(InlineKeyboardButton(text=_("Yo'q❌"), callback_data="convince:0"))
    return kb


def convince_btn_ru():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text="Ҳа✅", callback_data="convince:1"))
    kb.add(InlineKeyboardButton(text="Йўқ❌", callback_data="convince:0"))
    return kb