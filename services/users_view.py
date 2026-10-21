# services/users_view.py
from aiogram import html


def format_users_list(users: list[dict], title: str = "Пользователи") -> str:
    return f"<b>{html.quote(title)}</b> ({len(users)}):"


def format_user_card(user: dict) -> str:
    """Текст карточки. Одинаков для админа и работодателя."""
    return (
        f"👤 <b>{html.quote(user['full_Name'])}</b>\n"
        f"Роль: <b>{user['role']}</b>\n"
        f"Telegram ID: <code>{user['telegram_id']}</code>"
    )