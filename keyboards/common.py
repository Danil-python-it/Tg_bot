from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from config import SUPER_ADMIN_ID
from services.roles import has_permission


COMMON_BUTTONS = [
    ("⚙️ Настройки профиля"),
]

PERMISSION_BUTTONS = {
    "create_work":      ["➕ Добавить задачу"],
    "view_works":       ["💰 Мои начисления"],
    "view_price":       ["📋 Показать прайс"],
    "view_payouts":     ["💰 Общий расчёт"],
    "view_workers":     ["👥 лист сотрудников"],
    "manage_users":     ["👥 лист Пользователи"],
}

ADMINS_BUTTONS = [
    ("👥 лист Пользователи"),
]


def get_main_menu(user: dict) -> ReplyKeyboardMarkup:
    
    b = ReplyKeyboardBuilder()

    for _text in COMMON_BUTTONS:
        b.button(text=_text)

    for perm, container in PERMISSION_BUTTONS.items():
        if has_permission(user["role"], perm):
            for content in container:
                b.button(text=content)

    if user["telegram_id"] == SUPER_ADMIN_ID:
        for _text in ADMINS_BUTTONS:
            b.button(text=_text)
    
    b.adjust(1)
    return b.as_markup(resize_keyboard=True)

def get_users_list_kb(users: list[dict], prefix: str = "user") -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for u in users:
        b.button(
            text=f"{u['full_name']} — {u['role']}",
            callback_data=f"{prefix}:{u['telegram_id']}",
        )
    b.button(text="⬅️ Назад", callback_data=("common:back"))
    b.adjust(1)
    return b.as_markup()