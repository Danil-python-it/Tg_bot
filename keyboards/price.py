from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def get_price_list_kb(positions: list[dict], action: str = "edit") -> InlineKeyboardMarkup:

    b = InlineKeyboardBuilder()  
    for pos in positions:
        b.button(
            text=f"{pos['title']} — {pos['price']:.0f} ₽",
            callback_data=f"{action}:{pos['id']}",
        )
    b.adjust(1)  
    return b.as_markup()

def get_price_menu() -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    b.button(text="➕ Добавить позицию")
    b.button(text="📋 Показать прайс")
    b.button(text="✏️ Изменить цену")
    b.button(text="⬅️ Назад")
    b.adjust(2)
    return b.as_markup(resize_keyboard=True)
