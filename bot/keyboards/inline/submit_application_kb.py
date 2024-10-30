from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.utils.translation import gettext as _


submit_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=_("Tasdiqlash✅"), callback_data="submit"),
        ],
        [
            InlineKeyboardButton(text=_("Bekor qilish❌"), callback_data="cancel"),\
        ]
    ]
)