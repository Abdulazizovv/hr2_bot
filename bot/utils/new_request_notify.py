from bot.data.config import ADMINS
from aiogram import Dispatcher
import logging
from bot.utils.db_api import get_user_request
from asgiref.sync import sync_to_async
import asyncio


async def on_new_request_notify(dp: Dispatcher, request_id: int):
    for admin in ADMINS:
        try:
            await asyncio.sleep(0.5)
            data = await sync_to_async(get_user_request)(request_id)
            if not data:
                return None
            try:
                await dp.bot.send_document(chat_id=admin, document=data['file_id'], caption=f"Yangi ariza qabul qilindi:\n"
                                                f"⚜️Mebel sohasida {'ishlagan✅' if data['worked_furniture'] else 'ishlamagan❌'}\n"
                                                f"👤 Ismi: {data['full_name']}\n"
                                                f"📞 Telefon raqami: {data['phone_number']}\n"
                                                f"📅 Tug'ilgan yili: {data['birth_year']}\n"
                                                f"📍 Manzili: {data['region']}\n"
                                                f"🛂 Millati: {data['nationality']}")
            except Exception as err:
                logging.exception(err)

        except Exception as err:
            logging.exception(err)