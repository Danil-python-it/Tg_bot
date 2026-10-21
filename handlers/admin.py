from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from DB.users import get_user, set_role, get_all_users

from keyboards.admin import get_admin_menu
from keyboards.inline import get_users_list_kb, get_admin_user_card_kb

from services.users_view import format_users_list, format_user_card

from filters.AdminFilter import AdminFilter

router = Router()
router.message.filter(AdminFilter())
router.callback_query.filter(AdminFilter())

@router.message(F.text == "Сменить Роль")
async def set_role_user(message: Message, user:dict):    
    await set_role(user["telegram_id"], ("worker" if user["role"] == "employer" else "employer"))
    await message.answer(
        f"Теперь ваша роль - {"worker" if user["role"] == "employer" else "employer"}"
    )
    return

@router.message(F.text == "Список Пользователей")
async def get_all_user(message: Message, user:dict):
    users = await get_all_users()
    if not users:
        await message.answer("Людей здесь нет", reply_markup=get_admin_menu())
        return
    
    await message.answer(
        format_users_list(users),
        reply_markup=get_users_list_kb(users,'admin'),
    )

@router.callback_query(F.data.startswith("admin:"))
async def open_user_card(call: CallbackQuery):
    user_id = int(call.data.split(":")[1])
    user = await get_user(user_id)
    if user is None:
        await call.answer("Пользователь не найден", show_alert=True)
        return

    await call.message.edit_text(
        format_user_card(user),
        reply_markup=get_admin_user_card_kb(user_id, user["role"]),
    )
    await call.answer() 
    
@router.callback_query(F.data.startswith("role:set:"))
async def change_role(call: CallbackQuery):
    _, _, user_id_str, new_role = call.data.split(":")
    user_id = int(user_id_str)

    await set_role(user_id, new_role)   # ← функция в DB/users.py
    user = await get_user(user_id)

    await call.message.edit_text(
        f"👤 <b>{user['full_Name']}</b>\n"
        f"Роль: <b>{user['role']}</b>\n"
        f"Telegram ID: <code>{user['telegram_id']}</code>",
        reply_markup=get_admin_user_card_kb(user_id, user["role"]),
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
async def back_admin_menu(call: CallbackQuery):
    await call.message.delete()
    await call.answer(reply_markup=get_admin_menu())

@router.message(F.text == "admin menu")
async def get_a_menu(message: Message):
    await message.answer(
        f"menu:\n",
        reply_markup=get_admin_menu()
    )
    return
 