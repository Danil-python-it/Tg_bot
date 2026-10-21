from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_admin_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text="Сменить Роль")
    builder.button(text="Список Пользователей")

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
