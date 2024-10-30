from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


language_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Lotincha🇺🇿"),
            KeyboardButton("Krillcha🇷🇺")
        ],
    ],
    resize_keyboard=True
)