from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards._helpers import build_menu

buttons = {
    "permission_buttons":{
        "create_price":      ["➕ Добавить позицию","📋 Показать прайс"],
        "edit_price":        ["✏️ Изменить цену"],
    },
    "common_buttons":["⬅️ Назад"]
}

def get_price_list_kb(positions: list[dict], action: str = "edit") -> InlineKeyboardMarkup:

    b = InlineKeyboardBuilder()  
    for pos in positions:
        b.button(
            text=f"{pos['title']} — {pos['price']:.0f} ₽",
            callback_data=f"{action}:{pos['id']}",
        )
    b.adjust(1)  
    return b.as_markup()

def get_price_menu(user: dict) -> ReplyKeyboardMarkup:
    return build_menu(user, buttons, 2)
