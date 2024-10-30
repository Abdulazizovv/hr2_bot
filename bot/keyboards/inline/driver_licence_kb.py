from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.utils.translation import gettext as _


def driver_licence_btn():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text=_("A"), callback_data="driver_licence:A"))
    kb.add(InlineKeyboardButton(text=_("B"), callback_data="driver_licence:B"))
    kb.add(InlineKeyboardButton(text=_("B, C"), callback_data="driver_licence:BC"))
    kb.add(InlineKeyboardButton(text=_("Yo'q❌"), callback_data="driver_licence:Yoq"))
    kb.add(InlineKeyboardButton(text=_("Boshqa♻️"), callback_data="driver_licence:Boshqa"))
    return kb
    