from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject
from services.roles import has_permission

class PermissionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        required = get_flag(data, "permission")
        if required is None:
            return await handler(event, data)          # хендлер без флага — публичный

        user = data.get("user")
        if not user or not has_permission(user["role"], required):
            if hasattr(event, "answer"):
                await event.answer("⛔ Недостаточно прав.")
            return
        return await handler(event, data)