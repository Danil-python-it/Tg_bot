from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

class RoleFilter(BaseFilter):
    def __init__(self, role: str):
        self.role = role

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        from DB.users import get_user
        user = await get_user(event.from_user.id)
        return user is not None and user["role"] == self.role