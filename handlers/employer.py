from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from services.users_view import format_users_list, format_user_card
from services.works_view import format_works_list, format_works_dict

from keyboards.employer import get_employer_menu
from keyboards.inline import get_users_list_kb, get_employer_user_card_kb

from DB.users import get_all_users, get_user
from DB.works import get_all_works
from DB.worker_data import get_worker_data

router = Router()

@router.message(F.text == "лист рабочих")
async def get_all_user(message: Message):
    user = await get_user(message.from_user.id)

    if user["role"] != 'employer':
        await message.answer("Эта функция недоступна")
        return

    users = await get_all_users()
    if not users:
        await message.answer("Людей здесь нет", reply_markup=get_employer_menu())
        return

    workers = [user for user in users if user["role"] == "worker"]
    
    await message.answer(
        format_users_list(workers),
        reply_markup=get_users_list_kb(workers,'emp'),
    )

@router.callback_query(F.data.startswith("emp:"))
async def open_user_card(call: CallbackQuery):
    user_autor = await get_user(call.from_user.id)

    if user_autor["role"] != 'employer':
        await call.answer("Нет доступа", show_alert=True)
        return

    user_id = int(call.data.split(":")[1])
    user = await get_user(user_id)
    if user is None:
        await call.answer("Пользователь не найден", show_alert=True)
        return

    await call.message.edit_text(
        format_user_card(user),
        reply_markup=get_employer_user_card_kb(user_id),
    )
    await call.answer() 
    
@router.callback_query(F.data.startswith("works:"))
async def get_user_works(call: CallbackQuery):
    user_autor = await get_user(call.from_user.id)

    if user_autor["role"] != 'employer':
        await call.answer("Нет доступа", show_alert=True)
        return

    user_id = int(call.data.split(":")[1])
    user = await get_user(user_id)
    if user is None:
        await call.answer("Пользователь не найден", show_alert=True)
        return
    
    positions = await get_all_works(user["id"])
    salary = (await get_worker_data(user["id"]))["salary"]
    text = await format_works_list(positions,user["full_Name"],salary)

    await call.message.answer(text)
    await call.message.delete()
    await call.answer() 

@router.callback_query(F.data == "back:emp:list")
async def back_to_list(call: CallbackQuery):
    user_autor = await get_user(call.from_user.id)
    
    if user_autor["role"] != 'employer':
        await call.answer("Нет доступа", show_alert=True)
        return

    users = await get_all_users()
    await call.message.edit_text(
        format_users_list(users),
        reply_markup=get_users_list_kb(users,'emp'),
    )
    await call.answer()

@router.callback_query(F.data == "back:emp:menu")
async def back_to_menu(call: CallbackQuery):
    user_autor = await get_user(call.from_user.id)
    
    if user_autor["role"] != 'employer':
        await call.answer("Нет доступа", show_alert=True)
        return

    await call.message.delete()
    await call.answer(reply_markup=get_employer_menu())

@router.message(F.text == "Составить общий расчет")
async def get_all_calculations(message: Message):
    user = await get_user(message.from_user.id)

    if user["role"] != 'employer':
        await message.answer("Эта функция недоступна")
        return

    users = await get_all_users()
    if not users:
        await message.answer("Людей здесь нет", reply_markup=get_employer_menu())
        return

    workers = [user for user in users if user["role"] == "worker"]
    text = await format_works_dict(workers)
    await message.answer(
        text,
        reply_markup=get_employer_menu(),
    )
