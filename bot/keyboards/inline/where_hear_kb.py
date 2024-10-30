from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.utils.translation import gettext as _


def where_hear_btn():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=_("Telegram orqali"), callback_data="telegram"),
            InlineKeyboardButton(text=_("Instagram orqali"), callback_data="instagram"),
        ],
        [
            InlineKeyboardButton(text=_("Facebook orqali"), callback_data="facebook"),
            InlineKeyboardButton(text=_("Tanishim"), callback_data="tanishim"),
        ],
        [
            InlineKeyboardButton(text=_("Boshqa"), callback_data="boshqa"),
        ]
    ])
    return keyboard