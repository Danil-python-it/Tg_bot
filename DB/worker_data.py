from DB.database import get_db


async def get_worker_data(user_id: int) -> str | None:
    db = await get_db()

    async with db.execute("SELECT * FROM worker_data WHERE assignee_id = ?", (user_id,)) as cursor:
        row = await cursor.fetchone()
        return dict(row) if row else None

async def update_worker_salary(user_id: int, new_salary: int ) -> str | None:
    db = await get_db()
    await db.execute(
        "UPDATE worker_data SET salary = ? WHERE assignee_id = ?", (new_salary, user_id)
    )
    await db.commit()

async def add_worker_data_to_user(user_id: int) -> str | None:
    db = await get_db()
    cur = await db.execute(
        "INSERT OR IGNORE INTO worker_data (assignee_id, salary) VALUES (?, ?)",
        (user_id, 0),
    )
    await db.commit()
    return cur.lastrowid