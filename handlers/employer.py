from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from services.users_view import format_users_list, format_user_card
from services.works_view import format_works_list, format_works_dict

from keyboards.common import get_main_menu, get_users_list_kb
from keyboards.employer import get_employer_user_card_kb

from DB.users import get_all_users_with_role, get_user_to_telegram_id
from DB.works import get_all_works

from filters.RoleFilter import RoleFilter

router = Router()
router.message.filter(RoleFilter("employer"))
router.callback_query.filter(RoleFilter("employer"))

@router.message(F.text == "👥 лист рабочих")
async def get_all_user(message: Message, user:dict):
    workers = await get_all_users_with_role("worker")
    if not workers:
        await message.answer("Людей здесь нет", reply_markup=get_main_menu(user))
        return
    
    await message.answer(
        format_users_list(workers),
        reply_markup=get_users_list_kb(workers,'emp'),
    )

@router.callback_query(F.data.startswith("emp:"))
async def open_user_card(call: CallbackQuery):
    user_telegram_id = int(call.data.split(":")[1])
    user = await get_user_to_telegram_id(user_telegram_id)
    if user is None:
        await call.answer("Пользователь не найден", show_alert=True)
        return

    await call.message.edit_text(
        format_user_card(user),
        reply_markup=get_employer_user_card_kb(user_telegram_id),
    )
    await call.answer() 
    
@router.callback_query(F.data.startswith("works:"))
async def get_user_works(call: CallbackQuery):

    user_telegram_id = int(call.data.split(":")[1])
    user = await get_user_to_telegram_id(user_telegram_id)
    if user is None:
        await call.answer("Пользователь не найден", show_alert=True)
        return
    
    positions = await get_all_works(user["id"])
    text = await format_works_list(positions,user)

    await call.message.delete()
    await call.message.answer(text)
    await call.answer() 

@router.callback_query(F.data == "back:emp:list")
async def back_to_list(call: CallbackQuery):
    users = await get_all_users_with_role("worker")
    await call.message.edit_text(
        format_users_list(users),
        reply_markup=get_users_list_kb(users,'emp'),
    )
    await call.answer()

@router.message(F.text == "💰 Общий расчёт")
async def get_all_calculations(message: Message, user:dict):
    workers = await get_all_users_with_role("worker")
    if not workers:
        await message.answer("Людей здесь нет", reply_markup=get_main_menu(user))
        return

    text = await format_works_dict(workers)
    await message.answer(
        text,
        reply_markup=get_main_menu(user),
    )
