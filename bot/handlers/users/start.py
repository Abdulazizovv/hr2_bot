from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.loader import dp
from bot.keyboards.default import language_btn, main_menu_btn
from bot.utils.db_api import add_user, set_user_language
from asgiref.sync import sync_to_async
from django.utils import translation
from django.utils.translation import gettext as _
from bot.states import Language
from aiogram.dispatcher import FSMContext




@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = """
АССАЛОМУ АЛЕЙКУМ!!!    
СИЗНИ ҚАДРЛАЙДИГАН ЖАМОАДА ИШЛАШНИ ХОҲЛАЙСИЗМИ?   
            
Унда сиз учун АЖОЙИБ ИМКОНИЯТ!   
            
            
☝️ Сиздан ДИПЛОМ талаб қилинмайди!   
            
✳️ ИШ НИМАДАН ИБОРАТ:   
▪️Мижозлар билан киришимли булиш;   
▪️Краска сепиш
▪️Юмшоқ мебел устаси
▪️Мебел нолдан териб установка қилиш
            
            
            
✅ БИЗ, АЙНАН СИЗНИ ТАНЛАЙМИЗ, АГАР СИЗ:    
• 20-30 ёшдаги йигит бўлсангиз;   
• Хушмуомилали;   
• Жамоада ишлаш маҳорати;   
• Маълумотларга эътиборли;    
• Масьулиятли;   
            
            
            
😍 Сизни қандай ИМКОНИЯТЛАР кутмоқда БИЛАСИЗМИ?   
• Бир мақсад асосида йиғилган ЖАМОА аъзоси бўлиш;   
• Ойлик маошдан ташқари  БОНУСЛАРГА эга бўлиш имконияти;   
• Замонавий шинам офисда ишлаш;   
• Ўз вақтида ойлик маош   
• Расман ишга кабул қилиш;   
• Тажриба олиш имконияти;   
• Шахсий ривожланиш ва Карера қилиш;   
• Иш вакти: 8:30 - 19:30 гача. дам олиш вақтлари хафтада бир кун.
            
            
            
👧🏻 Агар сиз, инсонлар билан МУЛОҚОТ қилишни яхши кўрсангиз, СИЗ БИЗНИ САФИМИЗДАСИЗ!

ИЛТИМОС ҚИЛАМИЗ ҚУЙИДАГИ САВОЛЛАРГА АНИҚ МАЪЛУМОТ БЕРИНГ!
"""
    await sync_to_async(add_user)(user_id=message.from_user.id, username=message.from_user.username, full_name=message.from_user.full_name)
    await message.answer(text, reply_markup=language_btn)


@dp.message_handler(text=["Lotincha🇺🇿", "Krillcha🇷🇺"])
async def set_language(message: types.Message):
    language = "uz"
    if message.text == "Lotincha🇺🇿":
        language = "uz"
    elif message.text == "Krillcha🇷🇺":
        language = "ru"
    await sync_to_async(set_user_language)(user_id=message.from_user.id, language_code=language)
    translation.activate(language)
    await message.answer(_("Asosiy bo`limga xush keldingiz😊"), reply_markup=main_menu_btn)    

