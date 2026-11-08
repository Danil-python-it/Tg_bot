from aiogram.types import ReplyKeyboardMarkup

from keyboards._helpers import build_menu

buttons = {
    "common_buttons":["⬅️ Назад"],
    "permission_buttons":{
        "create_work":      ["➕ Добавить задачу"],
        "view_payouts":     ["💰 Мои начисления"],
    }
}

def get_works_menu(user:dict) -> ReplyKeyboardMarkup:
    return build_menu(user, buttons)
