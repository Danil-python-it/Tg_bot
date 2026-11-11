from DB.database import get_db


async def creaet_section(employer_id: int, name: str) -> float:
    db = await get_db()
    cur = await db.execute(
        "INSERT OR IGNORE INTO sections (name, employer_id) VALUES (?, ?)",
        (name, employer_id),
    )
    await db.commit()
    return cur.lastrowid

async def get_section(section_id: int) -> dict:
    db = await get_db()

    async with db.execute("SELECT * FROM sections WHERE id = ?", (section_id,)) as cursor:
        row = await cursor.fetchone()
        return dict(row) if row else None

async def get_section_to_employer(employer_id: int) -> dict:
    db = await get_db()
    
    async with db.execute("SELECT * FROM sections WHERE employer_id = ?", (employer_id,)) as cursor:
        row = await cursor.fetchone()
        return dict(row) if row else None

async def update_name_section(section_id: int, new_name: str) -> None:
    db = await get_db()
    await db.execute(
        "UPDATE sections SET name = ? WHERE id = ?", (new_name, section_id)
    )
    await db.commit()

async def update_employer_section(section_id: int, new_employer_id: int) -> None:
    db = await get_db()
    await db.execute(
        "UPDATE sections SET employer_id = ? WHERE id = ?", (new_employer_id, section_id)
    )
    await db.commit()

async def get_all_sections() -> list[dict]:
    db = await get_db()
    cur = await db.execute("SELECT * FROM sections")
    row = await cur.fetchall()  
    return [dict(r) for r in row]