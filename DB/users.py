#get_user, add_user, set_role, list_workers
from DB.database import get_db


async def get_user(user_id: int) -> str | None:
    """Возвращает роль пользователя или None, если его нет в базе."""
    db = await get_db()

    async with db.execute("SELECT * FROM users WHERE id = ?", (user_id,)) as cursor:
        row = await cursor.fetchone()
        return dict(row) if row else None
    
async def get_user_to_telegram_id(telegram_id: int) -> str | None:
    """Возвращает роль пользователя или None, если его нет в базе."""
    db = await get_db()

    async with db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)) as cursor:
        row = await cursor.fetchone()
        return dict(row) if row else None

async def add_user(telegram_id: int, full_name: str, role: str = "worker") -> int:
    db = await get_db()
    cur = await db.execute(
        "INSERT OR IGNORE INTO users (telegram_id, full_name, role) VALUES (?, ?, ?)",
        (telegram_id, full_name, role),
    )
    await db.commit()
    return cur.lastrowid

async def set_role(user_id: int, role: str) -> None:
    db = await get_db()
    await db.execute(
        "UPDATE users SET role = ? WHERE id = ?", (role, user_id)
    )
    await db.commit()

async def set_section(user_id: int, section_id: int) -> None:
    db = await get_db()
    await db.execute(
        "UPDATE users SET section_id = ? WHERE id = ?", (section_id, user_id)
    )
    await db.commit()

async def get_all_users(section_id:int = None) -> list[dict]:
    db = await get_db()
    if section_id is None: 
        cur = await db.execute("SELECT * FROM users")
    else: 
        cur = await db.execute("SELECT * FROM users WHERE section_id = ?",(section_id,))
    row = await cur.fetchall()  
    return [dict(r) for r in row]

async def get_all_users_with_role(section_id: int, role: str) -> list[dict]:
    db = await get_db()
    cur = await db.execute("SELECT * FROM users WHERE section_id = ? AND role = ?",(section_id, role))
    row = await cur.fetchall()  
    return [dict(r) for r in row]