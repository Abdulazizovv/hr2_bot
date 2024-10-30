from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.utils.translation import gettext as _


nationalities = [_("O'zbek"), _("Rus"),  _("Tojik"), _("Qozoq"), _("Qirg'iz"), _("Boshqa")]

def nationalities_btn():
    kb = InlineKeyboardMarkup(row_width=1)
    for index, nationality in enumerate(nationalities):
        kb.add(InlineKeyboardButton(text=nationality, callback_data=f"nationality:{index}"))
    return kb

