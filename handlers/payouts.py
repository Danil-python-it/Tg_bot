from aiogram import Router, F, flags
from aiogram.types import Message, CallbackQuery

from services.works import format_works_dict, format_works_list

from keyboards.common import get_main_menu
from keyboards.works import get_works_menu

from DB.users import get_all_users_with_role, get_user_to_telegram_id
from DB.works import get_all_works


router = Router()

@router.message(F.text == "💰 Общий расчёт")
@flags.permission("view_payouts")
async def get_all_calculations(message: Message, user:dict):
    workers = await get_all_users_with_role(user["section_id"], "worker")
    if not workers:
        await message.answer("Людей здесь нет", reply_markup=get_main_menu(user))
        return

    text = await format_works_dict(workers)
    await message.answer(
        text,
        reply_markup=get_main_menu(user),
    )

@router.message(F.text == "💰 Мои начисления")
@flags.permission("view_works")
async def show_works(message: Message, user: dict):
    positions = await get_all_works(user["section_id"], user["id"])
    text = await format_works_list(positions,user)

    await message.answer(
        text,
        reply_markup=get_works_menu(user)
    )

@router.callback_query(F.data.startswith("payout:"))
@flags.permission("view_works")
async def show_works_to_user(call: CallbackQuery):
    telegram_id = int(call.data.split(":")[1])
    user = await get_user_to_telegram_id(telegram_id)
    if user is None:
        await call.answer("Не найден", show_alert=True)
        return
    positions = await get_all_works(user["section_id"], user["id"])
    text = await format_works_list(positions,user)
    await call.message.answer(
        text
    )
    await call.answer()

