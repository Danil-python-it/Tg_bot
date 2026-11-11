#create_work, delete_work
from DB.database import get_db
from datetime import datetime

async def get_all_works(section_id: int, user_id: int) -> list[dict]:
    db = await get_db()
    async with db.execute(
        """
        SELECT price_list_item_id, rate_snapshot, count, assignee_id, work_date FROM works
        WHERE section_id = ? AND assignee_id = ?
        ORDER BY work_date 
    """,
        (section_id, user_id,)
    ) as cursor:
        rows = await cursor.fetchall()
    return [dict(r) for r in rows]

async def add_work(section_id:int, price_list_item_id: int,rate_snapshot: int, count: int, user_id: int, work_date: datetime,) -> int:
    db = await get_db()
    cur = await db.execute(
        "INSERT OR IGNORE INTO works (section_id, price_list_item_id,rate_snapshot,count,assignee_id,work_date) VALUES (?, ?, ?, ?, ?, ?)",
        (section_id, price_list_item_id, rate_snapshot, count, user_id, work_date),
    )
    await db.commit()
    return cur.lastrowid


    