from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def is_worked_kb():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Ha', callback_data='is_worked_yes'),
        InlineKeyboardButton(text='Yo\'q', callback_data='is_worked_no')
    )
    return markup