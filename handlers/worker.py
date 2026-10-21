# handlers/worker.py
from aiogram import html
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.work import AddWork

from keyboards.work_list import get_works_menu, get_cancel_menu
from keyboards.inline import get_price_list_kb
from keyboards.worker import get_current_data

from DB.users import get_user
from DB.price_list import get_price_list, get_price_position
from DB.works import (
    add_work,
    get_all_works
)
from DB.worker_data import (
    get_worker_data,
    update_worker_salary,
    add_worker_data_to_user
)


from services.works_view import format_works_list

router = Router()

CANCEL_TEXT = "❌ Отмена"

# ---------- Отмена (работает в любом состоянии) ----------

@router.message(F.text == CANCEL_TEXT)
async def cancel_any(message: Message, state: FSMContext):
    current = await state.get_state()
    if current is None:
        await message.answer("Нечего отменять.", reply_markup=get_works_menu())
        return
    await state.clear()
    await message.answer("Отменено.", reply_markup=get_works_menu())

@router.message(F.text == "➕ Добавить задачу")
async def add_user_work(message: Message, state: FSMContext):

    user = await get_user(message.from_user.id)
    if user["role"] != "worker":
        await message.answer("Эта функция доступна только работникам.")
        return
    
    user_worker_data = await get_worker_data(user["id"])
    if (user_worker_data) is None:
        await add_worker_data_to_user(user["id"])
        user_worker_data = await get_worker_data(user["id"])

    positions = await get_price_list()
    if not positions:
        await message.answer("Прайс пуст — обратитесь к работодателю.", reply_markup=get_works_menu())
        return

    await state.set_state(AddWork.waiting_position)
    await state.update_data(user_id=user["id"], salary=user_worker_data["salary"])
    await message.answer(
        "Выберите позицию:",
        reply_markup=get_price_list_kb(positions, action="GET")
    )

@router.callback_query(AddWork.waiting_position, F.data.startswith("GET:"))
async def work_choose_position(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])

    # Достаём позицию из прайса, чтобы знать title и price
    position = await get_price_position(position_id)
    if position is None:
        await call.answer("Позиция не найдена", show_alert=True)
        await state.clear()
        return

    await state.update_data(
        position_id=position_id,
        title=position["title"],
        price=position["price"]
    )
    await state.set_state(AddWork.waiting_count)

    # Убираем inline-список, показываем reply-клавиатуру с отменой
    await call.message.edit_text(
        f"Выбрано: «{position['title']}»\n"
        f"Введите колличество выполненых единиц (число):"
    )
    await call.message.answer("Жду колличество...", reply_markup=get_cancel_menu())
    await call.answer()

@router.message(AddWork.waiting_count)
async def work_count(message: Message, state: FSMContext):
    try:
        count = int(message.text.replace(",", ".").strip())
        if count <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Нужно положительное число. Ещё раз:")
        return

    data = await state.get_data()
    await state.update_data(count = count)
    await state.set_state(AddWork.waiting_date)
    await message.answer(
        f"Товар: {data["title"]}\n"
        f"Колличество: {count}\n"
        f"Введите дату выполнения (ГГГГ.ММ.ДД):",
        reply_markup=get_current_data()
    )    

@router.message(AddWork.waiting_date)
async def work_date(message: Message, state: FSMContext):
    from datetime import datetime
    try:
        datetime.strptime(message.text.replace(".","-").strip(), "%Y-%m-%d")
    except ValueError:
        await message.answer("Формат даты: ГГГГ.ММ.ДД (например, 2026.10.18). Ещё раз:")
        return 

    data = await state.get_data()
    await add_work(data["position_id"], data["count"], data["user_id"], message.text.replace(".","-").strip())
    await update_worker_salary(
        data["user_id"],
        (int(data["salary"])+(int(data["count"])*int(data["price"])))
    )

    await state.clear()
    await message.answer(
        f"Товар: {data["title"]}\n"
        f"Колличество: {data["count"]}\n"
        f"Введите дату выполнения {message.text.strip()}\n\n"
        "Задача сохранена",
        reply_markup=get_works_menu(),
    )

@router.message(F.text == "📋 Показать выполненные задачи")
async def show_works(message: Message):
    user = await get_user(message.from_user.id)
    
    if user["role"] != "worker":
        await message.answer("Эта функция доступна только работникам.")
        return

    positions = await get_all_works(user["id"])
    salary = (await get_worker_data(user["id"]))["salary"]
    text = await format_works_list(positions,user["full_Name"],salary)

    await message.answer(
        text,
        reply_markup=get_works_menu()
    )
    


