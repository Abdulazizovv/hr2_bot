from aiogram import types
from bot.keyboards.inline import married_btn
from bot.keyboards.inline import convince_btn
from bot.loader import dp
from django.utils.translation import gettext as _
from bot.states import RegisterState
from aiogram.dispatcher import FSMContext
from bot.keyboards.default import phone_number_btn, back_kb, main_menu_btn, cancel_btn, language_btn
from bot.keyboards.inline import positions_btn, start_request_btn, regions_btn, regions
from bot.keyboards.inline import nationalities_btn, nationalities, submit_btn
from asgiref.sync import sync_to_async
from bot.utils.db_api import get_all_positions, get_position, add_user_request
from botapp.models import Position
from bot.keyboards.inline import education_levels_btn, education_levels
from bot.keyboards.inline import driver_licence_btn
from bot.keyboards.inline import has_car_btn
from bot.keyboards.inline import degree_btn, skip_btn, where_hear_btn, is_worked_kb
import asyncio


@dp.message_handler(text="🔙 Orqaga", state="*")
@dp.message_handler(text="🔙 Орқага", state="*")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(_("Bosh sahifadasiz"), reply_markup=language_btn)


@dp.message_handler(text="Bekor qilish❌", state="*")
async def cancel_request(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(_("Ariza bekor qilindi"), reply_markup=main_menu_btn)


@dp.message_handler(commands="register")
@dp.message_handler(text="✍️ Ro'yxatdan o'tish")
@dp.message_handler(text="✍️ Рўйхатдан ўтиш")
async def user_register(message: types.Message):
    await message.answer(_("To'liq ism familyangizni kiriting:\nMasalan: Sobirov Olim"), reply_markup=cancel_btn)
    await RegisterState.full_name.set()


@dp.message_handler(state=RegisterState.full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer(_("Tug'ilgan kun, oy, yilingizni kiriting:\nMasalan: 01.01.1990"))
    await RegisterState.birth_year.set()


@dp.message_handler(state=RegisterState.birth_year)
async def get_birth_year(message: types.Message, state: FSMContext):
    await state.update_data(birth_year=message.text)
    await message.answer(_("Telefon raqamingizni yuboring"), reply_markup=phone_number_btn)
    await RegisterState.phone_number.set()


@dp.message_handler(state=RegisterState.phone_number, content_types=types.ContentType.CONTACT)
async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)

    await message.answer(_("Mebel sohasida ishlaganmisiz?"), reply_markup=is_worked_kb())
    await RegisterState.worked_furniture.set()


@dp.callback_query_handler(state=RegisterState.worked_furniture)
async def get_is_worked(call: types.CallbackQuery, state: FSMContext):
    is_worked = call.data
    if is_worked == "is_worked_yes":
        await state.update_data(worked_furniture="Ha")
    else:
        await state.update_data(worked_furniture="Yo'q")
    positions = await sync_to_async(lambda: list(Position.objects.all()), thread_sensitive=True)()

    if not positions:
        await call.message.delete()
        await call.message.answer(_("Hozircha hech qanday yo'nalish mavjud emas. Iltimos, keyinroq urinib ko'ring."), reply_markup=main_menu_btn)
        await state.finish()
        return

    await call.message.edit_text(_("Iltimos, soha bo'yicha yo'nalishni tanlang:"), reply_markup=positions_btn(positions))
    await RegisterState.position.set()



@dp.callback_query_handler(state=RegisterState.position)
async def get_position(call: types.CallbackQuery, state: FSMContext):
    position_id = call.data.split(":")[-1]
    position = await sync_to_async(lambda: Position.objects.filter(id=int(position_id)).first(), thread_sensitive=True)()
    await state.update_data(position=position.name)
    text = _("Anketa to'ldirishni boshlash✏️")
    if position:
        if position.description:
            text = position.description
    await call.message.edit_text(text, reply_markup=start_request_btn)
    await RegisterState.start_request.set()


@dp.callback_query_handler(state=RegisterState.start_request)
async def start_request(call: types.CallbackQuery, state: FSMContext):
    if call.data == "start_request":
        await call.message.edit_text(_("Qaysi viloyat yoki shahardansiz?"), reply_markup=regions_btn())
        await RegisterState.region.set()
    else:
        await call.message.edit_text(_("Ariza qoldirish bekor qilindi.\nSiz bosh sahifaga qaytdingiz."))
        await state.finish()

    
@dp.callback_query_handler(state=RegisterState.region)
async def get_region(call: types.CallbackQuery, state: FSMContext):
    region_index = call.data.split(":")[-1]
    region = regions[int(region_index)]
    await state.update_data(region=region)
    await call.message.edit_text(_("Millatingizni tanlang:"), reply_markup=nationalities_btn())
    await RegisterState.nationality.set()


@dp.callback_query_handler(state=RegisterState.nationality)
async def get_nationality(call: types.CallbackQuery, state: FSMContext):
    nationality_index = call.data.split(":")[-1]
    nationality = nationalities[int(nationality_index)]
    await state.update_data(nationality=nationality)
    await call.message.edit_text(_("Ma'lumotingiz:"), reply_markup=education_levels_btn())
    await RegisterState.education.set()


@dp.callback_query_handler(state=RegisterState.education)
async def get_education(call: types.CallbackQuery, state: FSMContext):
    education_index = call.data.split(":")[-1]
    data = await state.get_data()
    education = education_levels[int(education_index)]
    await state.update_data(education=education)
    await call.message.edit_text(_("Oilaviy holatingiz:"), reply_markup=married_btn())
    await RegisterState.marriage.set()


@dp.callback_query_handler(state=RegisterState.marriage)
async def get_marriage(call: types.CallbackQuery, state: FSMContext):
    marriage = call.data.split(":")[-1]
    await state.update_data(marriage="Turmush qurgan" if marriage=="1" else "Turmush qurmagan")
    await call.message.edit_text(_("Qaysi korxona yoki tashkilotlarda va qaysi lavozimlarda ishlagansiz?\n"
                                   "Masalan: OOO 'Uzavtosanoat' da, Direktor bo'lib ishlaganman\n"
                                   "<b><i>*Bu bo'limni to'ldirish majburiy</i></b>"))
    await RegisterState.first_answer.set()


@dp.message_handler(state=RegisterState.first_answer)
async def get_first_answer(message: types.Message, state: FSMContext):
    await state.update_data(first_answer=message.text)
    await message.answer(_("Bizda qancha maoshga ishlamoqchisiz?\n"
                           "Masalan: 2 000 000 so'm"))
    await RegisterState.salary.set()


@dp.message_handler(state=RegisterState.salary)
async def get_salary(message: types.Message, state: FSMContext):
    await state.update_data(salary=message.text)
    await message.answer(_("Bizning korxonada qancha muddat ishlamoqchisiz?\n"
                           "Masalan: 1 yil, 1 oy va h.k."))
    await RegisterState.second_answer.set()


@dp.message_handler(state=RegisterState.second_answer)
async def get_second_answer(message: types.Message, state: FSMContext):
    await state.update_data(second_answer=message.text)
    await message.answer(_("Sudlanganmisiz?"), reply_markup=convince_btn())
    await RegisterState.convince.set()


@dp.callback_query_handler(state=RegisterState.convince)
async def get_convince(call: types.CallbackQuery, state: FSMContext):
    convince = call.data.split(":")[-1]
    await state.update_data(convince="Sudlangan" if convince=="1" else "Sudlanmagan")
    await call.message.edit_text(_("Haydovchilik guvohnomangiz bormi?"), reply_markup=driver_licence_btn())
    await RegisterState.driver_license.set()


@dp.callback_query_handler(state=RegisterState.driver_license)
async def get_driver_license(call: types.CallbackQuery, state: FSMContext):
    driver_license = call.data.split(":")[-1]
    await state.update_data(driver_license=driver_license)
    await call.message.edit_text(_("O'zingizni shaxsiy avtomobilingiz bormi?"), reply_markup=has_car_btn())
    await RegisterState.has_car.set()


@dp.callback_query_handler(state=RegisterState.has_car)
async def get_has_car(call: types.CallbackQuery, state: FSMContext):
    has_car = call.data.split(":")[-1]
    await state.update_data(has_car="Bor" if has_car=="1" else "Yo'q")
    await call.message.edit_text(_("Rus tili bilish darajangizni tanlang:"), reply_markup=degree_btn())
    await RegisterState.russian_level.set()


@dp.callback_query_handler(state=RegisterState.russian_level)
async def get_russian_level(call: types.CallbackQuery, state: FSMContext):
    russian_level = call.data.split(":")[-1]
    await state.update_data(russian_level=f"{russian_level} %")
    await call.message.edit_text(_("Ingliz tili bilish darajangizni tanlang:"), reply_markup=degree_btn())
    await RegisterState.english_level.set()


@dp.callback_query_handler(state=RegisterState.english_level)
async def get_english_level(call: types.CallbackQuery, state: FSMContext):
    english_level = call.data.split(":")[-1]
    await state.update_data(english_level=f"{english_level} %")
    await call.message.edit_text(_("Boshqa tillarni bilasizmi?\nQaysi til va necha % "), reply_markup=skip_btn)
    await RegisterState.other_language.set()


@dp.callback_query_handler(state=RegisterState.other_language)
async def skip_other_language(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(other_language="Yo'q")
    await call.message.edit_text(_("Word dasturini bilish darajasi:\n(foizda(%) ko'rsating)"), reply_markup=degree_btn())
    await RegisterState.third_answer.set()


@dp.message_handler(state=RegisterState.other_language)
async def get_other_language(message: types.Message, state: FSMContext):
    await state.update_data(other_language=message.text)
    await message.answer(_("Word dasturini bilish darajasi:\n(foizda() ko'rsating)"), reply_markup=degree_btn())
    await RegisterState.third_answer.set()


@dp.callback_query_handler(state=RegisterState.third_answer)
async def get_third_answer(call: types.CallbackQuery, state: FSMContext):
    third_answer = call.data.split(":")[-1]
    await state.update_data(third_answer=f"{third_answer} %")
    await call.message.edit_text(_("Excel dasturini bilish darajasi:\n(foizda() ko'rsating)"), reply_markup=degree_btn())
    await RegisterState.fourth_answer.set()


@dp.callback_query_handler(state=RegisterState.fourth_answer)
async def get_excel_level(call: types.CallbackQuery, state: FSMContext):
    excel_level = call.data.split(":")[-1]
    await state.update_data(fourth_answer=f"{excel_level} %")
    await call.message.edit_text(_("1C dasturini bilish darajasi:\n(foizda() ko'rsating)"), reply_markup=degree_btn())
    await RegisterState.c1_program_level.set()


@dp.callback_query_handler(state=RegisterState.c1_program_level)
async def get_c1_program_level(call: types.CallbackQuery, state: FSMContext):
    c1_program_level = call.data.split(":")[-1]
    await state.update_data(c1_program_level=f"{c1_program_level} %")
    await call.message.edit_text(_("Boshqa qanday dasturlar bilan ishlay olasiz?\nNomi va necha %"), reply_markup=skip_btn)
    await RegisterState.fifth_answer.set()


@dp.callback_query_handler(state=RegisterState.fifth_answer)
async def skip_fifth_answer(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(fifth_answer="Yo'q")
    await call.message.edit_text(_("Korxonamiz haqida qayerdan ma'lumot oldingiz?"), reply_markup=where_hear_btn())
    await RegisterState.sixth_answer.set()


@dp.message_handler(state=RegisterState.fifth_answer)
async def get_fifth_answer(message: types.Message, state: FSMContext):
    await state.update_data(fifth_answer=message.text)
    await message.answer(_("Korxonamiz haqida qayerdan ma'lumot oldingiz?"), reply_markup=where_hear_btn())
    await RegisterState.sixth_answer.set()


@dp.callback_query_handler(state=RegisterState.sixth_answer)
async def get_sixth_answer(call: types.CallbackQuery, state: FSMContext):
    sixth_answer = call.data
    await state.update_data(sixth_answer=sixth_answer)
    await call.message.edit_text(_("Iltimos, rasmingizni yuboring:"))
    await RegisterState.image.set()


@dp.message_handler(state=RegisterState.image, content_types=types.ContentType.PHOTO)
async def get_image(message: types.Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    await message.answer_photo(data.get("image"), caption=_(f"<b>Ma'lumotlaringizni to'gri ekanligini tekshiring va tasdiqlang</b>\n\n" \
                           f"<b>Ism va familya:</b> {data.get('full_name')}\n"
                           f"<b>Tug'ilgan yil:</b> {data.get('birth_year')}\n"
                           f"<b>Telefon raqam:</b> {data.get('phone_number')}\n"
                           f"<b>Mebel sohasida ishlaganligi:</b> {data.get('worked_furniture')}\n"
                           f"<b>Lavozim:</b> {data.get('position')}\n"
                           f"<b>Hudud:</b> {data.get('region')}\n"
                           f"<b>Millat:</b> {data.get('nationality')}\n"
                           f"<b>Ma'lumoti:</b> {data.get('education')}\n"
                           f"<b>Oilaviy ahvol:</b> {data.get('marriage')}\n"
                           f"<b>Qaysi korxonalarda ishlaganligi:</b> {data.get('first_answer')}\n"
                           f"<b>Oylik maosh:</b> {data.get('salary')}\n"
                           f"<b>Ish muddati:</b> {data.get('second_answer')}\n"
                           f"<b>Sudlanganlik:</b> {data.get('convince')}\n"
                           f"<b>Haydovchilik guvohnomasi:</b> {data.get('driver_license')}\n"
                           f"<b>Shaxsiy avtomobil:</b> {data.get('has_car')}\n"
                            f"<b>Rus tili:</b> {data.get('russian_level')}\n"
                            f"<b>Ingliz tili:</b> {data.get('english_level')}\n"
                            f"<b>Boshqa tillar:</b> {data.get('other_language')}\n"
                            f"<b>Word dasturi:</b> {data.get('third_answer')}\n"
                            f"<b>Excel dasturi:</b> {data.get('fourth_answer')}\n"
                            f"<b>1C dasturi:</b> {data.get('c1_program_level')}\n"
                            f"<b>Boshqa dasturlar:</b> {data.get('fifth_answer')}\n"
                            f"<b>Qayerdan ma'lumot oldingiz:</b> {data.get('sixth_answer')}\n"
                           ), 
                           reply_markup=submit_btn
                           )


# Utility function to run an async function in a new event loop in a separate thread
def run_async_in_thread(async_func, *args):
    loop = asyncio.new_event_loop()  # Create a new event loop for the thread
    asyncio.set_event_loop(loop)  # Set it as the current loop for this thread
    loop.run_until_complete(async_func(*args))  # Run the async function
    loop.close()  # Close the loop when done


@dp.callback_query_handler(text=["submit", "cancel"], state="*")
async def submit_application(call: types.CallbackQuery, state: FSMContext):
    import threading
    from bot.utils.new_request_notify import on_new_request_notify
    if call.data == "submit":
        data = await state.get_data()

        from bot.utils.generate_pdf import create_pdf_with_tables, upload_to_channel
        file_name = f"{call.from_user.id}_data.pdf"
        image_stream = await dp.bot.download_file_by_id(data.get("image"))
        pdf = await create_pdf_with_tables(filename=file_name, data=data, image_stream=image_stream)
        caption_text = f"👤Ism sharif: {data.get('full_name')}" \
                        f"\n📞Telefon raqam: {data.get('phone_number')}" \
                        f"\n#️⃣Soha: {data.get('position')}" \
                        f"\n📍Hudud: {data.get('region')}"
        await call.message.edit_reply_markup()
        await call.message.answer("⏳")
        pdf_file_id, image_file_id = await upload_to_channel(pdf, data.get("image"), caption_text)
        request = await sync_to_async(add_user_request)(
            user_id=call.from_user.id,
            full_name=data.get("full_name"),
            phone_number=data.get("phone_number"),
            is_worked=True if data.get("worked_furniture")=="Ha" else False,
            birth_year=data.get("birth_year"),
            position=data.get("position"),
            region=data.get("region"),
            nationality=data.get("nationality"),
            education=data.get("education"),
            marriage=True if data.get("marriage")=="Turmush qurgan" else False,
            first_answer=data.get("first_answer"),
            salary=data.get("salary"),
            second_answer=data.get("second_answer"),
            convince=True if data.get("convince")=="Sudlangan" else False,
            driver_license=data.get("driver_license"),
            has_car=True if data.get("has_car")== "Bor" else False,
            russian_level=data.get("russian_level"),
            english_level=data.get("english_level"),
            other_language=data.get("other_language"),
            third_answer=data.get("third_answer"),
            fourth_answer=data.get("fourth_answer"),
            c1_program_level=data.get("c1_program_level"),
            fifth_answer=data.get("fifth_answer"),
            sixth_answer=data.get("sixth_answer"),
            image=image_file_id,
            file_id=pdf_file_id
        )
        
        await call.message.answer_document(document=pdf_file_id, caption=caption_text)
        await call.message.answer("Arizaningiz muvaffaqiyatli yuborildi✅")
        await on_new_request_notify(dp=dp, request_id=await sync_to_async(lambda: request.id)())
    else:
        await call.message.edit_reply_markup()
        await call.message.edit_text(_("Ariza yuborish bekor qilindi❌"))
    await state.finish()