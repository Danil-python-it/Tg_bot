from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_employer_user_card_kb(user_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="📋 Работы", callback_data=f"works:{user_id}")
    b.button(text="⬅️ К списку", callback_data="back:emp:list")
    b.adjust(1)
    return b.as_markup()