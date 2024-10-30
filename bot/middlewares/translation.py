from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from botapp.models import BotUser
from asgiref.sync import sync_to_async
from bot.utils.db_api import get_user
from django.utils import translation


class LanguageMiddleware(BaseMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def get_user_language(self, user_id: int) -> str:
        """Retrieve the user's language code from the database or return default."""
        user = await sync_to_async(get_user)(user_id)
        return user.language_code if user else 'uz'

    async def on_pre_process_message(self, message: Message, data: dict):
        language = await self.get_user_language(message.from_user.id)
        # print("Active language:", language)  # For debugging; can be removed in production
        translation.activate(language)
        data['language'] = language

    async def on_pre_process_callback_query(self, callback_query: CallbackQuery, data: dict):
        language = await self.get_user_language(callback_query.from_user.id)
        # print("Callback lang:", language)  # For debugging; can be removed in production
        translation.activate(language)
        data['language'] = language
