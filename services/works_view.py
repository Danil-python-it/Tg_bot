from datetime import datetime
from aiogram import html
from DB.price_list import get_price_position
from DB.works import get_all_works
from services.salary import get_user_calculation


async def format_works_list(positions: list[dict], user:dict, options:dict = {"isSalary":True}) -> str:
    user_name = user["full_name"]
    
    if not positions:
        return f"Лист работ у {user_name} пуст."

    lines = [f"<b>Лист работ</b> ({len(positions)} пун.):\n\n<b>{user_name}</b>"] if options["isSalary"] else [f"\n<b><u>{user_name}</u></b>"]
    last_date = ""
    index = 1
    for i, p in enumerate(positions, 1):
        title = (await get_price_position(p["price_list_item_id"]))["title"]
        try:
            d = datetime.strptime(p["work_date"], "%Y-%m-%d").strftime("%Y.%m.%d")
        except (ValueError, TypeError):
            d = p["work_date"] or "—"
        if last_date != d:
            lines.append(
                f"\n<b>{d}:</b>"
            )
            index = 1
            last_date = d

        lines.append(
            f"{index}. {title} — <b>{p['count']}шт.</b> "
        )
        index += 1

    salary = await get_user_calculation(user["id"])

    text = (f"{"\n".join(lines)}\n\n──────────\nЗаработал - <b>{salary}p</b>") if options["isSalary"]  else "\n".join(lines)

    return text

async def format_works_dict(users: list[dict]) -> str:
    if not users:
        return f"Список пуст."
    main_block = ["<b>Общий расчёт</b>:"]
    salares_block = []
    all_salares = 0

    for i, user in enumerate(users, 1):

        positions = await get_all_works(user["id"])
        user_calc = await format_works_list(positions, user, options={"isSalary":False})
        user_salary = await get_user_calculation(user["id"])

        if user_salary is None:
            salares_block.append(
                f"{i}. {user['full_name']} - список работ пуст"
            )
            continue 

        all_salares += user_salary

        main_block.append(user_calc)
        salares_block.append(
            f"{i}. <b>{user['full_name']}</b> заработал: <b>{user_salary}р.</b>"
        )

    return "\n".join(main_block) +"\n──────────\n"+ '\n'.join(salares_block) + f'\n\nВся сумма - <b>{all_salares}р.</b>'