from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.utils.translation import gettext as _


def positions_btn(positions):
    positions_kb = InlineKeyboardMarkup()
    for position in positions:
        positions_kb.add(InlineKeyboardButton(text=position.name, callback_data=f"position:{position.id}"))
    return positions_kb