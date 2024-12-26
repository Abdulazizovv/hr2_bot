from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from django.utils.translation import gettext as _


regions = [_("Toshkent"), _("Andijon"), _("Buxoro"), _("Farg'ona"), _("Jizzax"), _("Namangan"), _("Navoiy"), _("Qashqadaryo"), _("Qoraqalpog'iston Respublikasi"), _("Samarqand"), _("Sirdaryo"), _("Surxondaryo"), _("Toshkent viloyati"), _("Xorazm")]
fergana_regions = [_("Farg'ona shahri"), _("Qo'qon shahri"), _("Quvasoy shahri"), _("Marg'ilon shahri"), _("Oltiariq tumani"), _("Beshariq tumani"), _("Bag'dod tumani"), _("Buvayda tumani"), _("Dang'ara tumani"), _("Farg'ona tumani"), _("Furqat tumani"), _("Quva tumani"), _("Rishton tumani"), _("So'x tumani"), _("Toshloq tumani"), _("Uchko'prik tumani"), _("Yozyovon tumani"), _("Qo'shtepa tumani"), _("O'zbekiston tumani")]

def regions_btn():
    kb = InlineKeyboardMarkup(row_width=2)
    for region_id, region in enumerate(regions):
        kb.add(InlineKeyboardButton(text=region, callback_data=f"region:{region_id}"))
    return kb

def fergana_regions_btn():
    kb = InlineKeyboardMarkup(row_width=2)
    for region_id, region in enumerate(fergana_regions):
        kb.add(InlineKeyboardButton(text=region, callback_data=f"fergana_region:{region_id}"))
    return kb