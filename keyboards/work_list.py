from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_works_menu() -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    b.button(text="➕ Добавить задачу")
    b.button(text="📋 Показать выполненные задачи")
    b.button(text="⬅️ Назад")
    b.adjust(2)
    return b.as_markup(resize_keyboard=True)

def get_cancel_menu() -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    b.button(text="❌ Отмена")
    return b.as_markup(resize_keyboard=True)