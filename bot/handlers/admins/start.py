from aiogram import types
from bot.loader import dp
from bot.filters import IsAdmin
import logging
from bot.data.config import ADMINS
from asgiref.sync import sync_to_async
from botapp.models import UserRequest, BotUser, BotAdmin, Position
from datetime import datetime
from bot.keyboards.inline.admin_menu_kb import admin_menu_btn
from bot.utils.db_api import add_user


logger = logging.getLogger(__name__)

REQUESTS_PER_PAGE = 5

@dp.message_handler(IsAdmin(), commands=['start'])
async def admin_start(message: types.Message):
    try:
        await sync_to_async(add_user)(user_id=message.from_user.id, username=message.from_user.username, full_name=message.from_user.full_name)
        todays_requests = await sync_to_async(list)(UserRequest.objects.filter(created_at__date=datetime.now().date()))
        all_requests = await sync_to_async(list)(UserRequest.objects.all())
        all_users = await sync_to_async(list)(BotUser.objects.all())
        admins = await sync_to_async(list)(BotAdmin.objects.all())
        positions = await sync_to_async(list)(Position.objects.all())
        await message.answer(f"Assalomu alaykum, admin🫡\n"
                             f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                             f"Bugungi so'rovlar soni: {len(todays_requests)}\n"
                             f"Jami so'rovlar soni: {len(all_requests)}\n"
                             f"Jami foydalanuvchilar soni: {len(all_users)}\n"
                             f"Jami adminlar soni: {len(ADMINS)}\n"
                             f"Ochiq vakansiyalar soni: {len(positions)}\n"
                             f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n", reply_markup=admin_menu_btn)
    except Exception as e:
        logger.exception(f"Error in admin_start: {e}")
        await message.answer("Xatolik yuz berdi. Iltimos, keyinroq qaytadan urinib ko'ring.")

@dp.callback_query_handler(IsAdmin(), lambda call: call.data.startswith("requests"))
async def show_requests(call: types.CallbackQuery):
    try:
        page = int(call.data.split(":")[1]) if call.data.split(":")[1] else 0
        # Fetch all requests for pagination
        all_requests = await sync_to_async(list)(UserRequest.objects.all())
        total_requests = len(all_requests)

        # Calculate the current page of requests
        start_index = page * REQUESTS_PER_PAGE
        end_index = start_index + REQUESTS_PER_PAGE
        requests_to_display = all_requests[start_index:end_index]

        buttons = []
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        # Prepare the message
        if requests_to_display:
            requests_message = "Barcha arizalar:\n\n"
            for idx, request in enumerate(requests_to_display, start=start_index + 1):
                requests_message += f"{idx}. {request.full_name} - {request.position}\n"
                keyboard.insert(types.InlineKeyboardButton(f"{idx}", callback_data=f"request_detail:{request.id}"))
            
            # Create pagination buttons
            if start_index > 0:
                buttons.append(types.InlineKeyboardButton("Oldingi⬅️", callback_data=f"requests:{page - 1}"))
            if end_index < total_requests:
                buttons.append(types.InlineKeyboardButton("Keyingi➡️", callback_data=f"requests:{page + 1}"))

            keyboard.add(*buttons)
            keyboard.add(types.InlineKeyboardButton("Orqaga🔙", callback_data="start"))
            await call.message.delete()
            await call.message.answer(requests_message, reply_markup=keyboard)
        else:
            await call.message.edit_text("Arizalar topilmadi.")
    
    except Exception as e:
        logger.exception(f"Error in show_requests: {e}")
        await call.message.answer("Xatolik yuz berdi. Iltimos, keyinroq qaytadan urinib ko'ring.")


@dp.callback_query_handler(IsAdmin(), text="start", state="*")
async def back_to_start(call: types.CallbackQuery):
    await call.message.delete()
    await admin_start(call.message)


@dp.callback_query_handler(IsAdmin(), lambda call: call.data.startswith("request_detail:"))
async def show_request_detail(call: types.CallbackQuery):
    request_id = int(call.data.split(":")[1])
    try:
        request_detail = await sync_to_async(UserRequest.objects.get)(id=request_id)

        # Create a detailed message with enumerated fields
        detail_message = (
            f"Ariza ID: {request_detail.id}\n"
            f"1. Ism familyasi: {request_detail.full_name}\n"
            f"2. Telefon raqam: {request_detail.phone_number}\n"
            f"3. Tug'ilgan kun: {request_detail.birth_year}\n"
            f"4. Yo'nalish: {request_detail.position}\n"
            f"5. Hudud: {request_detail.region}\n"
            f"6. Millati: {request_detail.nationality}\n"
            f"7. Ma'lumoti: {request_detail.education}\n"
            f"8. Oilaviy holati: {'Turmush qurgan' if request_detail.marriage else 'Turmush qurmagan'}\n"
            f"9. Avval ishlagan korxonalar: {request_detail.first_answer if request_detail.first_answer else 'Mavjud emas'}\n"
            f"10. Kutayorgan maosh: {request_detail.salary}\n"
            f"11. Ishlash muddati: {request_detail.second_answer if request_detail.second_answer else 'N/A'}\n"
            f"12. Sudlanganmi: {'Ha' if request_detail.convince else 'Yo`q'}\n"
            f"13. Haydovchilik guvohnomasi: {request_detail.driver_license}\n"
            f"14. Mashinasi bormi: {'Yes' if request_detail.has_car else 'No'}\n"
            f"15. Ingliz tili darajasi: {request_detail.english_level}\n"
            f"16. Rus tili darajasi: {request_detail.russian_level}\n"
            f"17. Boshqa tillar: {request_detail.other_language}\n"
            f"18. Word dasturini bilish darajasi: {request_detail.third_answer}\n"
            f"19. Excel dasturini bilish darajsi: {request_detail.fourth_answer}\n"
            f"20. 1C dasturini bilish darajsi: {request_detail.c1_program_level}\n"
            f"21. Boshqa dasturlar: {request_detail.fifth_answer}\n"
            f"23. Biz haqimizda qayerdan ma'lumot oldi: {request_detail.sixth_answer if request_detail.sixth_answer else 'N/A'}\n"
            f"22. Mebel sohasida ishlaganmi:{'Ha' if request_detail.worked_furniture else 'Yo`q'}\n"
            f"24. Ariza yuborilgan sana: {request_detail.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

        try:
            await call.message.delete()
            kb = types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(text="Ariza fayli yuklash🗳", callback_data="get_request_file:{}".format(request_detail.id))
                    ]
                ]
            )
            if not request_detail.file_id:
                kb = None

            if request_detail.image:
                await call.message.answer_photo(request_detail.image, caption=detail_message, reply_markup=kb)
            else:
                await call.message.answer(detail_message, reply_markup=kb)
        except Exception as e:
            logging.error(f"Error in show_request_detail: {e}")
            await call.message.answer("Xatolik yuz berdi. Iltimos, keyinroq qaytadan urinib ko'ring.")
    except UserRequest.DoesNotExist:
        await call.message.answer("Request not found.")
    except Exception as e:
        logger.exception(f"Error in show_request_detail: {e}")
        await call.message.answer("Xatolik yuz berdi. Iltimos, keyinroq qaytadan urinib ko'ring.")


@dp.callback_query_handler(IsAdmin(), lambda call: call.data.startswith("get_request_file:"))
async def get_request_file(call: types.CallbackQuery):
    request_id = int(call.data.split(":")[1])
    try:
        await call.message.edit_reply_markup()
        request_detail = await sync_to_async(UserRequest.objects.get)(id=request_id)
        if request_detail.file_id:
            await call.message.answer_document(request_detail.file_id)
        else:
            await call.message.answer("Fayl topilmadi.")
    except UserRequest.DoesNotExist:
        await call.message.answer("Ariza topilmadi.")
    except Exception as e:
        logger.exception(f"Error in get_request_file: {e}")
        await call.message.answer("Xatolik yuz berdi. Iltimos, keyinroq qaytadan urinib ko'ring.")