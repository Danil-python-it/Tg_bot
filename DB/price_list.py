#create_work, delete_work
from DB.database import get_db

async def get_price_list(section_id:int,) -> list[dict]:
    """Все позиции, отсортированные по названию."""
    db = await get_db()
    async with db.execute(
        "SELECT id, title, price FROM price_list WHERE section_id = ? ORDER BY title COLLATE NOCASE",
        (section_id,)
    ) as cur:
        rows = await cur.fetchall()
    return [dict(r) for r in rows]

async def add_price_position(section_id:int, title: str,price: int) -> int:
    db = await get_db()
    cur = await db.execute(
        "INSERT OR IGNORE INTO price_list (section_id,title,price) VALUES (?, ?, ?)",
        (section_id, title, price),
    )
    await db.commit()
    return cur.lastrowid

async def get_price_position(section_id:int, position_id: int) -> dict | None:
    db = await get_db()
    async with db.execute(
        "SELECT id, title, price FROM price_list WHERE section_id = ? AND id = ?",
        (section_id, position_id)
    ) as cur:
        row = await cur.fetchone()
    return dict(row) if row else None

async def update_price(section_id:int, position_id: int, new_price: float) -> None:
    db = await get_db()
    await db.execute(
        "UPDATE price_list SET price = ? WHERE section_id = ? AND id = ?",
        (new_price, section_id, position_id),
    )
    await db.commit()

async def update_title(section_id:int, position_id: int, new_title: str) -> None:
    db = await get_db()
    await db.execute(
        "UPDATE price_list SET title = ? WHERE section_id = ? AND id = ?",
        (new_title, section_id, position_id),
    )
    await db.commit()

async def delete_price(section_id:int, position_id: int) -> None:
    db = await get_db()
    await db.execute(
        "DELETE FROM price_list WHERE section_id = ? AND id = ?",
        (section_id, position_id)
    )
    await db.commit()
