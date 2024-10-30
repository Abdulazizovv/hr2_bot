from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from django.utils.translation import gettext as _


regions = [_("Toshkent"), _("Andijon"), _("Buxoro"), _("Farg'ona"), _("Jizzax"), _("Namangan"), _("Navoiy"), _("Qashqadaryo"), _("Qoraqalpog'iston Respublikasi"), _("Samarqand"), _("Sirdaryo"), _("Surxondaryo"), _("Toshkent viloyati"), _("Xorazm")]


def regions_btn():
    kb = InlineKeyboardMarkup(row_width=2)
    for region_id, region in enumerate(regions):
        kb.add(InlineKeyboardButton(text=region, callback_data=f"region:{region_id}"))
    return kb