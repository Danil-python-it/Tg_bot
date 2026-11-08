from DB.database import get_db
from datetime import datetime

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