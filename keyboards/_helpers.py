# keyboards/_helpers.py
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from roles import has_permission
from config import SUPER_ADMIN_ID

def build_menu( 
        user: dict,
        buttons: dict = {
            "common_buttons":["⬅️ Назад"]
        },
        adjust: int = 1
    ) -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()

    if "common_buttons" in buttons:
        for _text in buttons["common_buttons"]:
                b.button(text=_text)
                
    if "permission_buttons" in buttons:
        for perm, container in buttons["permission_buttons"].items():
            if has_permission(user["role"], perm):
                for content in container:
                    b.button(text=content)

    if "developer_buttons" in buttons and user["telegram_id"] == SUPER_ADMIN_ID:
            for content in buttons["developer_buttons"]: 
                b.button(text=content)    

    b.adjust(adjust)
    return b.as_markup(resize_keyboard=True)