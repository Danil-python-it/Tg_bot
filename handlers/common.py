#common

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from DB.users import get_user, add_user

from keyboards.worker import get_worker_menu
from keyboards.employer import get_employer_menu

from config import SUPER_ADMIN_ID

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    tg_id = message.from_user.id
    user = await get_user(tg_id)

    # 1. Если пользователя нет — создаём
    if user is None:
        await add_user(tg_id, message.from_user.full_name, role="worker")
        user = await get_user(tg_id)
        
    await message.answer("Привет! Меню:", reply_markup= (get_worker_menu() if user["role"] == "worker" else get_employer_menu()))


@router.message(F.text == "status")
async def get_user_status(message: Message):
    tg_id = message.from_user.id
    user = await get_user(tg_id)

    await message.answer(
        f"Ваш статус - \n"
        f"<b>{user["full_Name"]}</b>\nДолжность - <b>{user["role"]}</b>\n\n"
        f"{"<b>SUPER ADMIN</b>" if tg_id == SUPER_ADMIN_ID else ""}"
        )
    return

@router.message(F.text == "/menu")
async def get_user_status(message: Message):
    tg_id = message.from_user.id
    user = await get_user(tg_id)

    if user["role"] == "worker":
        await message.answer("menu:\n", reply_markup=get_worker_menu())
    else:
        await message.answer("menu:\n", reply_markup=get_employer_menu())
    return

@router.message(F.text == "⬅️ Назад")
async def get_user_status(message: Message):
    tg_id = message.from_user.id
    user = await get_user(tg_id)

    if user["role"] == "worker":
        await message.answer("menu:", reply_markup=get_worker_menu())
    else:
        await message.answer("menu:", reply_markup=get_employer_menu())
    return
