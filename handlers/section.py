from aiogram import Router, F, flags
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from DB.sections import (
    creaet_section,
    get_section,
    get_section_to_employer,
    update_name_section,
    update_employer_section,
    get_all_sections
)

from DB.users import set_role, set_section, get_user, get_all_users
from keyboards.section import get_section_menu, get_sections_list_kb
from keyboards.fsm import get_cancel_menu
from keyboards.users import get_users_list_kb

from states.section import UpdateNameSection, UpdateEmployerSection


router = Router()


@router.message(F.text == "Создать компанию")
async def create_new_section(message: Message, user: dict):
    
    section_name = f"{user["full_name"]} company"

    await creaet_section(user["id"], section_name)
    
    section = await get_section_to_employer(user["id"])
    
    await set_role(user["id"],"employer")
    await set_section(user["id"], section["id"])

    await message.answer(
        f"Компания - <b>{section_name}</b>\nРуководитель - <b>{user["full_name"]}</b>",
        reply_markup=get_section_menu(user)
    )

@router.message(F.text == "Параметры компании")
async def create_new_section(message: Message, user: dict):

    section = await get_section_to_employer(user["id"])
    emp_name = user["full_name"] if user["id"] == section["employer_id"] else (await get_user(section["employer_id"]))["full_name"]
    await message.answer(
        f"Компания - <b>{section["name"]}</b>\nРуководитель - <b>{emp_name}</b>",
        reply_markup=get_section_menu(user)
    )

@router.message(F.text == "Изменить имя компании")
@flags.permission("edit_section")
async def start_update_name_section(message: Message, user: dict, state:FSMContext):

    section = await get_section_to_employer(user["id"])
    await state.set_state(UpdateNameSection.waiting_title)

    await message.answer(f"Старое название - |{section['name']}|\n\nВведите новое название", reply_markup=get_cancel_menu())

@router.message(UpdateNameSection.waiting_title)
@flags.permission("edit_section")
async def save_name(message: Message, state: FSMContext, user: dict):
    await update_name_section(user["section_id"], message.text)
    await state.clear()
    await message.answer("Имя обновлено",reply_markup=get_section_menu(user))

@router.message(F.text == "Поменять руководителя")
@flags.permission("edit_section")
async def update_employer_id(message: Message, user: dict, state: FSMContext):

    section = await get_section_to_employer(user["id"])
    emp_name = user["full_name"]

    if section["employer_id"] != user["id"]:
        await message.answer("Вы не владелец, эта функция вам не доступна")
        return

    await state.set_state(UpdateEmployerSection.waiting_choice)

    users = await get_all_users(section["id"])
    
    await message.answer(
        f"<b>{section['name']}</b>\nТекущий руководитель - |{emp_name}|\nЕго айди тг - |{user['telegram_id']}|\n\nВыберите другого пользователя:",
        reply_markup=get_users_list_kb(users,'new_emp')
    )

@router.callback_query(UpdateEmployerSection.waiting_choice, F.data.startswith("emp_new:"))
@flags.permission("edit_section")
async def save_name(call: CallbackQuery, state: FSMContext, user: dict):
    new_emp_id = int(call.data.split(":")[1])
    new_emp = await get_user(new_emp_id)
    await update_employer_section(user["section_id"], new_emp_id)
    if(new_emp["role"] != "employer"): await set_role(new_emp_id, "employer")
    await state.clear()
    await call.message.delete()
    await call.message.answer("Работодатель изменён",reply_markup=get_section_menu(user))

@router.message(F.text == "Компании")
async def view_all_sections(message: Message, user: dict):
    sections = await get_all_sections()

    if not sections:
        await message.answer("cписок компаний пуст.")
        return

    await message.answer(
        f"Лист компаний ({len(sections)})\b",
        reply_markup=get_sections_list_kb(sections)
    )

@router.callback_query(F.data.startswith("sup_admin:section:"))
async def save_name(call: CallbackQuery, user: dict):
    section_id = int(call.data.split(":")[2])
    section = await get_section(section_id)
    emp_name = (await get_user(section["employer_id"]))["full_name"]
    await call.message.delete()
    await call.message.answer(
        f"Компания - <b>{section["name"]}</b>\nРуководитель - <b>{emp_name}</b>",
        reply_markup=get_section_menu(user)
    )