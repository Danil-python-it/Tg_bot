from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config import SUPER_ADMIN_ID
from keyboards.keyboards_config import *

def get_main_menu(user: dict) -> ReplyKeyboardMarkup:
    
    b = ReplyKeyboardBuilder()

    for _text in COMMON_BUTTONS:
        b.button(text=_text)

    for _text in ROLE_BUTTONS.get(user["role"], []):
        b.button(text=_text)

    if user["telegram_id"] == SUPER_ADMIN_ID:
        for _text in ADMINS_BUTTONS:
            b.button(text=_text)
    
    b.adjust(1)
    return b.as_markup(resize_keyboard=True)

