from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_price_list_kb(positions: list[dict], action: str = "edit") -> InlineKeyboardMarkup:

    b = InlineKeyboardBuilder()
    for pos in positions:
        b.button(
            text=f"{pos['title']} — {pos['price']:.0f} ₽",
            callback_data=f"{action}:{pos['id']}",
        )
    b.adjust(1)  # по одной в ряд — длинные названия
    return b.as_markup()

def get_users_list_kb(users: list[dict], prefix: str = "user") -> InlineKeyboardMarkup:
    """
    prefix: 'admin' → callback 'admin:5'
            'emp'   → callback 'emp:5'
    """
    b = InlineKeyboardBuilder()
    for u in users:
        b.button(
            text=f"{u['full_Name']} — {u['role']}",
            callback_data=f"{prefix}:{u['telegram_id']}",
        )
    b.button(text="⬅️ Назад", callback_data=f"back:{prefix}:menu")
    b.adjust(1)
    return b.as_markup()


def get_admin_user_card_kb(user_id: int, current_role: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    next_role = "worker" if current_role == "employer" else "employer"
    b.button(text=f"🔄 Сделать {next_role}", callback_data=f"role:set:{user_id}:{next_role}")
    b.button(text="🗑 Удалить", callback_data=f"user:delete:{user_id}")
    b.button(text="⬅️ К списку", callback_data="back:admin:list")
    b.adjust(1)
    return b.as_markup()


def get_employer_user_card_kb(user_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="📋 Работы", callback_data=f"works:{user_id}")
    # b.button(text="➕ Назначить задачу", callback_data=f"task:{user_id}")
    b.button(text="⬅️ К списку", callback_data="back:emp:list")
    b.adjust(1)
    return b.as_markup()