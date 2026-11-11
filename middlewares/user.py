from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from DB.users import get_user_to_telegram_id
from DB.sections import get_section

class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        # Пытаемся достать telegram_id из события (Message или CallbackQuery)
        user_telegram_id = None
        if isinstance(event, Message):
            user_telegram_id = event.from_user.id
        elif hasattr(event, "from_user") and event.from_user: # CallbackQuery
            user_telegram_id = event.from_user.id

        if user_telegram_id:
            user = await get_user_to_telegram_id(user_telegram_id)
            if user:   
                section = await get_section(user["section_id"])            
                data["user"] = user  # 👈 Кладём в контекст
                data["section"] = section if section is not None else None

        # Передаём управление дальше (хендлеру)
        return await handler(event, data)