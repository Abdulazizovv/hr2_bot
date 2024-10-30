from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.utils.translation import gettext as _


start_request_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=_("Anketa to'ldirish🚀"), callback_data="start_request")
        ],
        [
            InlineKeyboardButton(text=_("Bekor qilish❌"), callback_data="cancel_request")
        ]
    ]
)