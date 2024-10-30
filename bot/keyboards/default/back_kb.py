from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


back_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔙 Orqaga")
        ]
    ],
    resize_keyboard=True
)