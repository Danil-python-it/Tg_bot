from aiogram import Router, F, flags
from aiogram.types import Message, CallbackQuery

from DB.users import get_user_to_telegram_id, set_role, get_all_users, get_all_users_with_role

from keyboards.users import get_admin_user_card_kb, get_users_list_kb
from keyboards.common import get_main_menu

from services.users_view import format_users_list, format_user_card
from roles import ROLES

router = Router()

@router.message(F.text == "👥 лист сотрудников")
@flags.permission("view_users")
async def list_workers(message: Message, user: dict):
    workers = await get_all_users_with_role(user["section_id"], "worker")
    if not workers:
        await message.answer("Работников нет.", reply_markup=get_main_menu(user))
        return
    await message.answer(
        format_users_list(workers, "Работники"),
        reply_markup=get_users_list_kb(workers, "emp"),
    )


@router.message(F.text == "👥 Пользователи")
@flags.permission("manage_users")
async def list_all_users(message: Message, user: dict):
    users = await get_all_users()
    if not users:
        await message.answer("Пользователей нет.", reply_markup=get_main_menu(user))
        return
    await message.answer(
        format_users_list(users, "Пользователи"),
        reply_markup=get_users_list_kb(users, "admin"),
    )

@router.callback_query(F.data.regexp(r"^admin:\d+$"))
@flags.permission("manage_users")
async def admin_user_card(call: CallbackQuery):
    telegram_id = int(call.data.split(":")[1])
    user = await get_user_to_telegram_id(telegram_id)
    if user is None:
        await call.answer("Не найден", show_alert=True)
        return
    await call.message.edit_text(
        format_user_card(user),
        reply_markup=get_admin_user_card_kb(telegram_id, user["role"]),
    )
    await call.answer()

@router.callback_query(F.data.startswith("emp:"))
@flags.permission("view_users")
async def employer_user_card(call: CallbackQuery):
    telegram_id = int(call.data.split(":")[1])
    user = await get_user_to_telegram_id(telegram_id)
    if user is None:
        await call.answer("Не найден", show_alert=True)
        return
    from keyboards.users import get_employer_user_card_kb
    await call.message.edit_text(
        format_user_card(user),
        reply_markup=get_employer_user_card_kb(telegram_id),
    )
    await call.answer()


@router.callback_query(F.data.startswith("role:set:"))
@flags.permission("manage_users")
async def change_role(call: CallbackQuery):
    _, _, tid_str, new_role = call.data.split(":")
    telegram_id = int(tid_str)
    if new_role not in ROLES:
        await call.answer("Неизвестная роль", show_alert=True)
        return
    user = await get_user_to_telegram_id(telegram_id)
    if user is None:
        await call.answer("Не найден", show_alert=True)
        return
    await set_role(user["id"], new_role)
    user = await get_user_to_telegram_id(telegram_id)
    await call.message.edit_text(
        format_user_card(user),
        reply_markup=get_admin_user_card_kb(telegram_id, new_role),
    )
    await call.answer(f"Роль изменена на {new_role}")


@router.callback_query(F.data == "back:admin:list")
@flags.permission("manage_users")
async def back_admin_list(call: CallbackQuery):
    users = await get_all_users()
    await call.message.edit_text(
        format_users_list(users, "Пользователи"),
        reply_markup=get_users_list_kb(users, "admin"),
    )
    await call.answer()


@router.callback_query(F.data == "back:emp:list")
@flags.permission("view_users")
async def back_emp_list(call: CallbackQuery, section: dict):
    workers = await get_all_users_with_role(section["id"], "worker")
    await call.message.edit_text(
        format_users_list(workers, "Работники"),
        reply_markup=get_users_list_kb(workers, "emp"),
    )
    await call.answer()