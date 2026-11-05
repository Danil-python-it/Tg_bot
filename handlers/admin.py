from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from DB.users import get_user_to_telegram_id, set_role, get_all_users

from keyboards.replay_menu import get_main_menu
from keyboards.inline_menu import get_users_list_kb, get_admin_user_card_kb

from services.users_view import format_users_list, format_user_card

from filters.AdminFilter import AdminFilter

router = Router()
router.message.filter(AdminFilter())
router.callback_query.filter(AdminFilter())

@router.message(F.text == "Сменить Роль")
async def set_role_user(message: Message, user:dict):    
    await set_role(user["id"], ("worker" if user["role"] == "employer" else "employer"))
    await message.answer(
        f"Теперь ваша роль - {"worker" if user["role"] == "employer" else "employer"}"
    )
    return

@router.message(F.text == "👥 Пользователи")
async def get_all_user(message: Message, user:dict):
    users = await get_all_users()
    if not users:
        await message.answer("Людей здесь нет", reply_markup=get_main_menu(user))
        return
    
    await message.answer(
        format_users_list(users),
        reply_markup=get_users_list_kb(users,'admin'),
    )

@router.callback_query(F.data.startswith("admin:"))
async def open_user_card(call: CallbackQuery):
    telegram_user_id = int(call.data.split(":")[1])
    user = await get_user_to_telegram_id(telegram_user_id)
    if user is None:
        await call.answer("Пользователь не найден", show_alert=True)
        return

    await call.message.edit_text(
        format_user_card(user),
        reply_markup=get_admin_user_card_kb(telegram_user_id, user["role"]),
    )
    await call.answer() 
    
@router.callback_query(F.data.startswith("role:set:"))
async def change_role(call: CallbackQuery):
    _, _, user_id_str, new_role = call.data.split(":")
    telegram_user_id = int(user_id_str)

    user = await get_user_to_telegram_id(telegram_user_id)
    await set_role(user["id"], new_role)
    
    user = await get_user_to_telegram_id(telegram_user_id)

    await call.message.edit_text(
        f"👤 <b>{user['full_name']}</b>\n"
        f"Роль: <b>{user['role']}</b>\n"
        f"Telegram ID: <code>{user['telegram_id']}</code>",
        reply_markup=get_admin_user_card_kb(telegram_user_id, user["role"]),
    )
    await call.answer(f"Роль изменена на {new_role}")

@router.callback_query(F.data == "back:admin:list")
async def back_to_list(call: CallbackQuery):
    users = await get_all_users()
    await call.message.edit_text(
        format_users_list(users),
        reply_markup=get_users_list_kb(users,"admin"),
    )
    await call.answer()

@router.callback_query(F.data == "back:admin:menu")
async def back_admin_menu(call: CallbackQuery, user:dict):
    await call.message.delete()
    await call.answer(
        "меню:",
        reply_markup=get_main_menu(user)
    )