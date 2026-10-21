from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_employer_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text="📋 Показать прайс")
    builder.button(text="лист рабочих")
    builder.button(text="Составить общий расчет")

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)