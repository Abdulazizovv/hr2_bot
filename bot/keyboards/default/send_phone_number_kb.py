from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from django.utils.translation import gettext as _


phone_number_btn = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(_("📞Telefon raqamni yuborish"), request_contact=True)
        ]
    ]
)