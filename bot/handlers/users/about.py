from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.loader import dp
from django.utils.translation import gettext as _


@dp.message_handler(text=["📑 Korxona haqida to'liq ma'lumot"])
async def about_company(message: types.Message):
    await message.answer(_("Buyurtma bo'yicha mijozlar hohishiga qarab turli xil mebel yasab beramiz\n"
                           "Ijtimoiy tarmoqdagi sahifalarimiz:\n"
                           "Instagram: 👉[Usta Abdulaziz](https://www.instagram.com/usta_abdulaziz?igshid=MWQ0MnFjY2ViOWhwNA%3D%3D&utm_source=qr)\n"
                           ), parse_mode="Markdown")