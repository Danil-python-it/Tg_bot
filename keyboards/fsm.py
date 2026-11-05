from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from datetime import date

def get_cancel_menu() -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    b.button(text="❌ Отмена")
    return b.as_markup(resize_keyboard=True)

def get_current_data() -> ReplyKeyboardMarkup:
    
    today = date.today()
    formatted_date = today.strftime("%Y.%m.%d")

    builder = ReplyKeyboardBuilder()

    builder.button(text=f"{formatted_date}")

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)