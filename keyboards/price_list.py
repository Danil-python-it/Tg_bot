from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_price_menu() -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    b.button(text="➕ Добавить позицию")
    b.button(text="📋 Показать прайс")
    b.button(text="✏️ Изменить цену")
    b.button(text="⬅️ Назад")
    b.adjust(2)
    return b.as_markup(resize_keyboard=True)

def get_cancel_menu() -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    b.button(text="❌ Отмена")
    return b.as_markup(resize_keyboard=True)