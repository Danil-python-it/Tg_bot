from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from DB.users import get_user_to_telegram_id, add_user

from keyboards.common import get_main_menu

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    tg_id = message.from_user.id
    user = await get_user_to_telegram_id(tg_id)

    # 1. Если пользователя нет — создаём
    if user is None:
        await add_user(tg_id, message.from_user.full_name, role="unknown")
        user = await get_user_to_telegram_id(tg_id)
        
    await message.answer("Привет! Меню:", reply_markup=get_main_menu(user))

@router.message(F.text.in_({"/menu","⬅️ Назад"}))
async def get_menu(message: Message, user:dict):
    await message.answer("меню:\n", reply_markup=get_main_menu(user))
    return

@router.callback_query(F.data == "common:back")
async def back_to_menu(call: CallbackQuery, user:dict):
    await call.message.delete()
    await call.message.answer(
        "меню:",
        reply_markup=get_main_menu(user)
        )
    await call.answer()