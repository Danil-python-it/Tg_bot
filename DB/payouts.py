from DB.database import get_db
from datetime import datetime

async def get_worker_salary(section_id: int, worker_id: int) -> float:
    db = await get_db()
    async with db.execute(
        "SELECT COALESCE(SUM(count * rate_snapshot), 0) AS total "
        "FROM works WHERE section_id = ? AND assignee_id = ?",
        (section_id, worker_id),
    ) as cur:
        row = await cur.fetchone()
    return float(row["total"])

async def get_total_salary(section_id: int) -> float:
    db = await get_db()
    async with db.execute(
        "SELECT COALESCE(SUM(count * rate_snapshot), 0) AS total FROM works WHERE section_id = ?",
        (section_id,)
    ) as cur:
        row = await cur.fetchone()
    return float(row["total"])