# handlers/price.py
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states.price import AddPrice, EditPrice
from keyboards.price_list import get_price_menu, get_cancel_menu
from keyboards.inline import get_price_list_kb
from DB.price_list import (
    add_price_position,
    get_price_list,
    get_price_position,
    update_price,
)

router = Router()

CANCEL_TEXT = "❌ Отмена"


# ---------- Отмена (работает в любом состоянии) ----------

@router.message(F.text == CANCEL_TEXT)
async def cancel_any(message: Message, state: FSMContext):
    current = await state.get_state()
    if current is None:
        await message.answer("Нечего отменять.", reply_markup=get_price_menu())
        return
    await state.clear()
    await message.answer("Отменено.", reply_markup=get_price_menu())


# ---------- Добавление ----------

@router.message(F.text == "➕ Добавить позицию")
async def start_add(message: Message, state: FSMContext):
    await state.set_state(AddPrice.waiting_title)
    await message.answer(
        "Введите название позиции (или нажмите «Отмена»):",
        reply_markup=get_cancel_menu(),
    )


@router.message(AddPrice.waiting_title)
async def add_title(message: Message, state: FSMContext):
    title = message.text.strip()
    if not title:
        await message.answer("Название не может быть пустым. Ещё раз:")
        return
    await state.update_data(title=title)
    await state.set_state(AddPrice.waiting_price)
    await message.answer("Введите цену (число, например 1500):")


@router.message(AddPrice.waiting_price)
async def add_price(message: Message, state: FSMContext):
    try:
        price = float(message.text.replace(",", ".").strip())
        if price < 0:
            raise ValueError
    except ValueError:
        await message.answer("Нужно неотрицательное число. Ещё раз:")
        return

    data = await state.get_data()
    try:
        await add_price_position(data["title"], price)
    except Exception:
        # Скорее всего, UNIQUE-конфликт по title
        await message.answer(
            f"Позиция «{data['title']}» уже есть в прайсе.",
            reply_markup=get_price_menu(),
        )
        await state.clear()
        return

    await state.clear()
    await message.answer(
        f"Добавлено: «{data['title']}» — {price:.0f} ₽",
        reply_markup=get_price_menu(),
    )


# ---------- Список позиций ----------

@router.message(F.text == "📋 Показать прайс")
async def show_price(message: Message):
    positions = await get_price_list()
    if not positions:
        await message.answer("Прайс пуст.", reply_markup=get_price_menu())
        return

    lines = [f"<b>Прайс-лист</b> ({len(positions)} поз.):\n"]
    for i, p in enumerate(positions, 1):
        lines.append(f"{i}. {p['title']} — <b>{p['price']:.0f} ₽</b>")
    await message.answer("\n".join(lines), reply_markup=get_price_menu())


# ---------- Редактирование: выбор позиции ----------

@router.message(F.text == "✏️ Изменить цену")
async def start_edit(message: Message, state: FSMContext):
    positions = await get_price_list()
    if not positions:
        await message.answer("Прайс пуст — нечего менять.", reply_markup=get_price_menu())
        return

    await state.set_state(EditPrice.waiting_choice)
    await message.answer(
        "Выберите позицию:",
        reply_markup=get_price_list_kb(positions, action="edit"),
    )


@router.callback_query(EditPrice.waiting_choice, F.data.startswith("edit:"))
async def edit_choose(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    position = await get_price_position(position_id)
    if position is None:
        await call.answer("Позиция не найдена", show_alert=True)
        await state.clear()
        return

    await state.update_data(position_id=position_id, title=position["title"])
    await state.set_state(EditPrice.waiting_new_price)
    await call.message.edit_text(
        f"«{position['title']}» — сейчас {position['price']:.0f} ₽.\n"
        f"Введите новую цену (или «{CANCEL_TEXT}»):"
    )
    # Показываем reply-клавиатуру с отменой (inline уже не нужен)
    await call.message.answer("Жду цену...", reply_markup=get_cancel_menu())
    await call.answer()


@router.message(EditPrice.waiting_new_price)
async def edit_new_price(message: Message, state: FSMContext):
    try:
        new_price = float(message.text.replace(",", ".").strip())
        if new_price < 0:
            raise ValueError
    except ValueError:
        await message.answer("Нужно неотрицательное число. Ещё раз:")
        return

    data = await state.get_data()
    await update_price(data["position_id"], new_price)
    await state.clear()
    await message.answer(
        f"Обновлено: «{data['title']}» — {new_price:.0f} ₽",
        reply_markup=get_price_menu(),
    )