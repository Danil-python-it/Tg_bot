from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from config import SUPER_ADMIN_ID

class AdminFilter(BaseFilter):
    def __init__(self):
        self.admin_id = SUPER_ADMIN_ID

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        from DB.users import get_user
        user = await get_user(event.from_user.id)
        return user is not None and user["telegram_id"] == self.admin_id