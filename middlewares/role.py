from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject


class RoleMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        required_role = get_flag(data, "role")

        if required_role is None:
            return await handler(event, data)
        
        user = data.get("user")
        
        if not user or user.get("role") != required_role:
            if hasattr(event, "answer"):
                await event.answer("⛔ Недостаточно прав для этого действия.")
            return 
        return await handler(event, data)