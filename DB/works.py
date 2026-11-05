#create_work, delete_work
from DB.database import get_db
from datetime import datetime

async def get_all_works(user_id: int) -> list[dict]:
    db = await get_db()
    async with db.execute(
        """
        SELECT price_list_item_id, rate_snapshot, count, assignee_id, work_date FROM works
        WHERE assignee_id = ?
        ORDER BY work_date 
    """,
        (user_id,)
    ) as cursor:
        rows = await cursor.fetchall()
    return [dict(r) for r in rows]

async def add_work(price_list_item_id: int,rate_snapshot: int, count: int, user_id: int, work_date: datetime,) -> int:
    db = await get_db()
    cur = await db.execute(
        "INSERT OR IGNORE INTO works (price_list_item_id,rate_snapshot,count,assignee_id,work_date) VALUES (?, ?, ?, ?, ?)",
        (price_list_item_id, rate_snapshot, count, user_id, work_date),
    )
    await db.commit()
    return cur.lastrowid

async def get_worker_salary(worker_id: int) -> float:
    db = await get_db()
    async with db.execute(
        "SELECT COALESCE(SUM(count * rate_snapshot), 0) AS total "
        "FROM works WHERE assignee_id = ?",
        (worker_id,),
    ) as cur:
        row = await cur.fetchone()
    return float(row["total"])

async def get_total_salary() -> float:
    db = await get_db()
    async with db.execute(
        "SELECT COALESCE(SUM(count * rate_snapshot), 0) AS total FROM works"
    ) as cur:
        row = await cur.fetchone()
    return float(row["total"])