from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards._helpers import build_menu


def get_section_menu(user:dict) -> ReplyKeyboardMarkup:
    buttons = {
        "common_buttons":["⬅️ Назад"],
        "permission_buttons":{
            "edit_section":["Изменить имя компании", "Поменять руководителя","Создать пригласительную ссылку","Список пользователей"],
        }
    }

    return build_menu(user, buttons)

def get_sections_list_kb(sections: list[dict]) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for section in sections:
        b.button(
            text=f"{section['name']}",
            callback_data=f"{'sup_admin:section'}:{section['id']}",
        )
    b.button(text="⬅️ Назад", callback_data=("common:back"))
    b.adjust(1)
    return b.as_markup()