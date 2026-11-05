from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_admin_user_card_kb(user_id: int, current_role: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    next_role = "worker" if current_role == "employer" else "employer"
    b.button(text=f"🔄 Сделать {next_role}", callback_data=f"role:set:{user_id}:{next_role}")
    # b.button(text="🗑 Удалить", callback_data=f"user:delete:{user_id}")
    b.button(text="⬅️ К списку", callback_data="back:admin:list")
    b.adjust(1)
    return b.as_markup()