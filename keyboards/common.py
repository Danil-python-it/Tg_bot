from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from config import SUPER_ADMIN_ID


COMMON_BUTTONS = [
    ("⚙️ Настройки профиля"),
]

ROLE_BUTTONS = {
    "employer": [
        ("📋 Показать прайс"),
        ("👥 лист рабочих"),
        ("💰 Общий расчёт"),
    ],
    "worker": [
        ("➕ Добавить задачу"),
        ("📋 Показать выполненные задачи"),
    ],
}

ADMINS_BUTTONS = [
    ("👥 Пользователи"),
    ("Сменить Роль"),
]


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