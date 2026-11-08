from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards._helpers import build_menu
from roles import ROLES

def get_profile_user(user:dict) -> ReplyKeyboardMarkup:
    buttons = {
        "commons_buttons":["⬅️ Назад"]
    }
    return build_menu(user, buttons)

def get_employer_user_card_kb(user_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="📋 Работы", callback_data=f"payout:{user_id}")
    b.button(text="⬅️ К списку", callback_data="back:emp:list")
    b.adjust(1)
    return b.as_markup()

def get_admin_user_card_kb(telegram_id: int, current_role: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for role_key, meta in ROLES.items():
        if role_key == current_role:
            continue
        b.button(
            text=f"{meta['emoji']} Сделать {meta['label']}",
            callback_data=f"role:set:{telegram_id}:{role_key}",
        )
    b.button(text="⬅️ К списку", callback_data="back:admin:list")
    b.adjust(1)
    return b.as_markup()

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