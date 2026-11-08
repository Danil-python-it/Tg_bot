from aiogram.types import ReplyKeyboardMarkup
from keyboards._helpers import build_menu

buttons = {
    "common_buttons": [
        ("⚙️ Настройки профиля"),
    ],
    "permission_buttons":{
        "create_work":      ["➕ Добавить задачу"],
        "view_works":       ["💰 Мои начисления"],
        "view_price":       ["📋 Показать прайс"],
        "view_payouts":     ["💰 Общий расчёт"],
        "view_workers":     ["👥 лист сотрудников"],
        "manage_users":     ["👥 Пользователи"],
    },
    "developer_buttons": ["👥 Пользователи"],
}

def get_main_menu(user: dict) -> ReplyKeyboardMarkup:
    return build_menu(user, buttons)