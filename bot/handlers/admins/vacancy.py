from aiogram import types
from bot.loader import dp
from bot.filters import IsAdmin
import logging
from asgiref.sync import sync_to_async
from botapp.models import Position
from bot.states.admin_state import AdminState
from aiogram.dispatcher import FSMContext

logger = logging.getLogger(__name__)

POSITIONS_PER_PAGE = 10

@dp.callback_query_handler(IsAdmin(), text="positions")
async def show_positions(call: types.CallbackQuery, page: int = 0):
    try:
        # Fetch all positions from the database
        all_positions = await sync_to_async(list)(Position.objects.all())
        total_positions = len(all_positions)

        # Calculate start and end indices for pagination
        start_index = page * POSITIONS_PER_PAGE
        end_index = start_index + POSITIONS_PER_PAGE
        positions_to_display = all_positions[start_index:end_index]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.insert(types.InlineKeyboardButton("Yangi vakansiya qo'shish➕", callback_data="add_position"))
        

        # Prepare the message
        if positions_to_display:
            positions_message = "Vakansiyalar:\n\n"
            for idx, position in enumerate(positions_to_display, start=start_index + 1):
                positions_message += f"{idx}. {position.name} - {position.description if position.description else ''}\n"
                keyboard.add(types.InlineKeyboardButton(f"{idx}", callback_data=f"position_detail:{position.id}"))
            # Create pagination buttons
            buttons = []
            if start_index > 0:
                buttons.append(types.InlineKeyboardButton("Previous", callback_data=f"show_positions:{page - 1}"))
            if end_index < total_positions:
                buttons.append(types.InlineKeyboardButton("Next", callback_data=f"show_positions:{page + 1}"))

            keyboard.add(*buttons)
            keyboard.add(types.InlineKeyboardButton("Orqaga", callback_data="start"))

            # Edit the original message with the updated positions and keyboard
            await call.message.edit_text(positions_message, reply_markup=keyboard)
        else:
            await call.message.answer("Vakansiyalar mavjud emas.", reply_markup=keyboard)
    
    except Exception as e:
        logger.exception(f"Error in show_positions: {e}")
        await call.message.answer("Xatolik yuz berdi. Iltimos, keyinroq qaytadan urinib ko'ring.")

@dp.callback_query_handler(IsAdmin(), lambda call: call.data.startswith("show_positions:"))
async def handle_position_pagination(call: types.CallbackQuery):
    page = int(call.data.split(":")[1])  # Extract the page number from callback data
    await call.answer()  # Acknowledge the callback to avoid loading issues

    # Call show_positions with the new page number
    await show_positions(call, page)


@dp.callback_query_handler(IsAdmin(), text="add_position")
async def add_position(call: types.CallbackQuery):
    try:
        await call.message.delete()
    except Exception as e:
        logger.exception(f"Error in add_position: {e}")
    await call.message.answer("Yangi vakansiya nomini kiriting:")
    await AdminState.new_position_name.set()


@dp.message_handler(IsAdmin(), state=AdminState.new_position_name)
async def save_position(message: types.Message, state):
    position_name = message.text
    await state.update_data(position_name=position_name)
    await message.answer("Vakansiya haqida ma'lumot kiriting:")
    await AdminState.new_position_description.set()


@dp.message_handler(IsAdmin(), state=AdminState.new_position_description)
async def save_position_description(message: types.Message, state):
    position_description = message.text
    position_name = (await state.get_data()).get("position_name")
    if position_name:
        position = await sync_to_async(Position.objects.create)(name=position_name, description=position_description)
        if position:
            await message.answer("Vakansiya saqlandi.")
        else:
            await message.answer("Vakansiyani saqlashda xatolik yuz berdi.")
    else:
        await message.answer("Vakansiya nomini kiriting.")
        await AdminState.new_position_name.set()
    await state.finish()
    await message.answer("Vakansiya saqlandi. /start orqali bosh menuga qayting.")


@dp.callback_query_handler(IsAdmin(), lambda call: call.data.startswith("position_detail:"))
async def show_position_detail(call: types.CallbackQuery):
    position_id = int(call.data.split(":")[1])
    position = await sync_to_async(Position.objects.get)(id=position_id)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("O'zgartirish", callback_data=f"edit_position:{position.id}"))
    keyboard.add(types.InlineKeyboardButton("O'chirish", callback_data=f"delete_position:{position.id}"))
    keyboard.add(types.InlineKeyboardButton("Orqaga", callback_data="positions"))
    if position:
        await call.message.edit_text(f"{position.name} - {position.description if position.description else ''}", reply_markup=keyboard)
    else:
        await call.message.answer("Vakansiya topilmadi.")
    await call.answer()


@dp.callback_query_handler(IsAdmin(), lambda call: call.data.startswith("edit_position:"))
async def edit_position(call: types.CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    await state.update_data(position_id=position_id)
    await call.message.answer("Yangi vakansiya nomini kiriting:")
    await call.message.edit_reply_markup()
    await AdminState.edit_position_name.set()


@dp.message_handler(IsAdmin(), state=AdminState.edit_position_name)
async def save_edited_position_name(message: types.Message, state):
    position_name = message.text
    await state.update_data(position_name=position_name)
    await message.answer("Vakansiya haqida ma'lumot kiriting:")
    await AdminState.edit_position_description.set()


@dp.message_handler(IsAdmin(), state=AdminState.edit_position_description)
async def save_edited_position_description(message: types.Message, state):
    position_description = message.text
    data = await state.get_data()
    position_name = data.get("position_name")
    position_id = data.get("position_id")
    if position_name:
        position = await sync_to_async(Position.objects.get)(id=position_id)
        position.name = position_name
        position.description = position_description
        await sync_to_async(position.save)()
        await message.answer("Vakansiya o'zgartirildi.")
    else:
        await message.answer("Vakansiya nomini kiriting.")
        await AdminState.edit_position_name.set()
    await state.finish()
    await message.answer("Vakansiya o'zgartirildi. /start orqali bosh menuga qayting.")


@dp.callback_query_handler(IsAdmin(), lambda call: call.data.startswith("delete_position:"))
async def delete_position(call: types.CallbackQuery):
    position_id = int(call.data.split(":")[1])
    position = await sync_to_async(Position.objects.get)(id=position_id)
    if position:
        await sync_to_async(position.delete)()
        await call.message.answer("Vakansiya o'chirildi.")
    else:
        await call.message.answer("Vakansiya topilmadi.")
    await call.answer()
    await show_positions(call)