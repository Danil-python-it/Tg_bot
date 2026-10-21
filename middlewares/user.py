from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from DB.users import get_user

class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        # Пытаемся достать telegram_id из события (Message или CallbackQuery)
        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif hasattr(event, "from_user") and event.from_user: # CallbackQuery
            user_id = event.from_user.id

        if user_id:
            user = await get_user(user_id)
            if user:
                data["user"] = user  # 👈 Кладём в контекст

        # Передаём управление дальше (хендлеру)
        return await handler(event, data)