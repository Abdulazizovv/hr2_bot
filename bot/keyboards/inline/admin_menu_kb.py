from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.utils.translation import gettext as _


admin_menu_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=_("Arizalar🗂"), callback_data="requests:0")
        ],
        # [
        #     InlineKeyboardButton(text=_("Vakansiyalar📋"), callback_data="positions")
        # ],
        [
            InlineKeyboardButton(text=_("Adminlar👨🏻‍💻"), callback_data="admins")
        ],

    ]
)