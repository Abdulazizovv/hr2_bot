from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from django.utils.translation import gettext as _



main_menu_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(_("✍️ Ro'yxatdan o'tish")),
            KeyboardButton(_("📑 Korxona haqida to'liq ma'lumot"))
        ],
        [
            KeyboardButton(_("🔙 Orqaga"))
        ]
    ],
    resize_keyboard=True
)