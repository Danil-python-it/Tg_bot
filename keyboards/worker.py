from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from datetime import date

def get_worker_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text="➕ Добавить задачу")
    builder.button(text="📋 Показать выполненные задачи")

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)

def get_current_data() -> ReplyKeyboardMarkup:
    
    today = date.today()
    formatted_date = today.strftime("%Y.%m.%d")

    builder = ReplyKeyboardBuilder()

    builder.button(text=f"{formatted_date}")

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)