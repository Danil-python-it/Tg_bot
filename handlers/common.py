#common

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from DB.users import get_user, add_user

from keyboards.replay_menu import get_main_menu

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    tg_id = message.from_user.id
    user = await get_user(tg_id)

    # 1. Если пользователя нет — создаём
    if user is None:
        await add_user(tg_id, message.from_user.full_name, role="worker")
        user = await get_user(tg_id)
        
    await message.answer("Привет! Меню:", reply_markup=get_main_menu(user))

@router.message(F.text == "/menu")
async def get_menu(message: Message, user:dict):
    await message.answer("menu:\n", reply_markup=get_main_menu(user))
    return

@router.message(F.text == "⬅️ Назад")
async def get_user_status(message: Message, user:dict):
    await message.answer("menu:\n", reply_markup=get_main_menu(user))
    return
