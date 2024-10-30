from aiogram import types
from bot.loader import dp
from bot.filters import IsAdmin
import logging
from asgiref.sync import sync_to_async
from botapp.models import BotAdmin, BotUser
from bot.states.admin_state import AdminState
from aiogram.dispatcher import FSMContext
from bot.keyboards.default.cancel_kb import cancel_btn
from bot.utils.db_api.db import add_bot_admin, remove_bot_admin
from bot.keyboards.inline import admin_menu_btn



logger = logging.getLogger(__name__)

from asgiref.sync import sync_to_async

@dp.callback_query_handler(IsAdmin(), text="admins")
async def show_admins(call: types.CallbackQuery):
    try:
        all_admins = await sync_to_async(list)(BotUser.objects.filter(is_admin=True))
        total_admins = len(all_admins)
        
        # Create a keyboard with an "Add Admin" button
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton("Yangi admin qo'shish➕", callback_data="add_admin"))

        # Prepare the message with the list of admins
        if all_admins:
            admins_message = "Adminlar:\n\n"
            for idx, admin in enumerate(all_admins, start=1):
                admins_message += f"{idx}. {admin.full_name} - {admin.user_id}\n"
                keyboard.insert(types.InlineKeyboardButton(admin.full_name, callback_data=f"admin_detail:{admin.id}"))
            keyboard.add(types.InlineKeyboardButton("Orqaga⬅️", callback_data="back_to_admin_menu"))
            await call.message.edit_text(admins_message, reply_markup=keyboard)
        else:
            keyboard.add(types.InlineKeyboardButton("Orqaga⬅️", callback_data="back_to_admin_menu"))
            await call.message.edit_text("Hozircha adminlar yo'q.", reply_markup=keyboard)
    except Exception as e:
        logger.exception(f"Error in show_admins: {e}")
        await call.message.answer("Xatolik yuz berdi. Iltimos, keyinroq qaytadan urinib ko'ring.")


@dp.callback_query_handler(IsAdmin(), text="back_to_admin_menu")
async def back_to_admin_menu(call: types.CallbackQuery):
    await call.message.edit_text("Admin menyuga qaytish", reply_markup=admin_menu_btn)


@dp.callback_query_handler(IsAdmin(), lambda call: call.data.startswith("admin_detail:"))
async def show_admin_detail(call: types.CallbackQuery):
    admin_id = int(call.data.split(":")[1])
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Olib tashlash❌", callback_data="admin_remove:" + str(admin_id)))
    keyboard.add(types.InlineKeyboardButton("Orqaga⬅️", callback_data="admins"))
    try:
        # Fetch specific admin details
        admin = await sync_to_async(BotUser.objects.get)(id=admin_id)
        admin_details = (
            f"Admin haqida ma'lumotlar:\n\n"
            f"👤 Ismi: {admin.full_name}\n"
            f"🆔 ID raqami: {admin.user_id}\n"
            f"📅 Ro'yxatdan o'tgan sana: {admin.created_at}\n"
            f"🔗 Profil: @{admin.username}" if admin.username else ''
        )
        await call.message.edit_text(admin_details, reply_markup=keyboard)
    except BotAdmin.DoesNotExist:
        await call.message.answer("Bunday admin topilmadi.", reply_markup=keyboard)
    except Exception as e:
        logger.exception(f"Error in show_admin_detail: {e}")
        await call.message.answer("Xatolik yuz berdi. Iltimos, keyinroq qaytadan urinib ko'ring.")


@dp.callback_query_handler(IsAdmin(), text="add_admin")
async def add_admin(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Yangi admin qo'shish uchun foydalanuvchi ID raqamini kiriting:", reply_markup=cancel_btn)
    await AdminState.new_admin_id.set()


@dp.message_handler(IsAdmin(), state=AdminState.new_admin_id)
async def set_new_admin_id(message: types.Message, state: FSMContext):
    try:
        new_admin_id = int(message.text)
        user = await sync_to_async(BotUser.objects.get)(user_id=new_admin_id)

        if user:
            # Create a new admin entry for the given user
            await sync_to_async(add_bot_admin)(user_id=new_admin_id)
            
            await message.answer("Yangi admin muvaffaqiyatli qo'shildi✅")
            await message.answer("Bosh sahifaga qaytish uchun /start buyrug'ini bosing.")
        else:
            await message.answer("Bunday foydalanuvchi topilmadi. Iltimos, foydalanuvchi ID raqamini tekshiring.")
    except ValueError:
        await message.answer("ID raqami noto'g'ri formatda kiritildi. Iltimos, faqat raqam kiriting.")
    except BotUser.DoesNotExist:
        await message.answer("Bunday foydalanuvchi topilmadi. Iltimos, foydalanuvchi ID raqamini tekshiring.")
    except Exception as e:
        logger.exception(f"Error in set_new_admin_id: {e}")
        await message.answer("Xatolik yuz berdi. Iltimos, keyinroq qaytadan urinib ko'ring.")
    finally:
        await state.finish()  # End the state after handling the message


@dp.message_handler(IsAdmin(), text="Bekor qilish❌", state=AdminState.new_admin_id)
async def cancel_adding_admin(message: types.Message, state: FSMContext):
    await message.answer("Admin qo'shish bekor qilindi❌")
    await message.answer("Bosh sahifaga qaytish uchun /start buyrug'ini bosing.")
    await state.finish()


@dp.callback_query_handler(IsAdmin(), lambda call: call.data.startswith("admin_remove:"))
async def remove_admin(call: types.CallbackQuery):
    admin_id = int(call.data.split(":")[1])
    try:
        admin = await sync_to_async(remove_bot_admin)(admin_id)
        if admin:
            await call.message.edit_text("Admin muvaffaqiyatli olib tashlandi❌", reply_markup=admin_menu_btn)
        else:
            await call.message.answer("Bunday admin topilmadi.", reply_markup=admin_menu_btn)
    except BotUser.DoesNotExist:
        await call.message.answer("Bunday admin topilmadi.", reply_markup=admin_menu_btn)
    except Exception as e:
        logger.exception(f"Error in remove_admin: {e}")
        await call.message.answer("Xatolik yuz berdi. Iltimos, keyinroq qaytadan urinib ko'ring.")