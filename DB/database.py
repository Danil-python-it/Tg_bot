import aiosqlite
from pathlib import Path
from config import DB_PATH

# Глобальное соединение (создаётся один раз)
_connection: aiosqlite.Connection | None = None

async def get_db() -> aiosqlite.Connection:
    """Возвращает ЕДИНОЕ соединение. Создаёт при первом вызове."""
    global _connection
    if _connection is None:
        _connection = await aiosqlite.connect(DB_PATH)
        _connection.row_factory = aiosqlite.Row  # доступ по имени столбца
        await _connection.execute("PRAGMA foreign_keys = ON")
        await _connection.execute("PRAGMA journal_mode = WAL")
    return _connection

async def init_db():
    """Создает таблицу, если её нет."""
    async with aiosqlite.connect(DB_PATH) as db:
        # Включаем внешние ключи (важно для SQLite)
        await db.execute("PRAGMA foreign_keys = ON")
        
        # Простейшая таблица для примера (потом заменишь на свою схему)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                full_Name   TEXT   DEFAULT 'unknown',
                role        TEXT   DEFAULT 'worker',
                created_at  TEXT DEFAULT (datetime('now'))
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS price_list (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                title      TEXT NOT NULL UNIQUE,
                price      REAL NOT NULL CHECK (price >= 0),
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS works (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                price_list_item_id  INTEGER REFERENCES price_list(id),
                rate_snapshot       REAL, 
                count               INTEGER,
                assignee_id         INTEGER REFERENCES users(id),
                work_date           TEXT NOT NULL,  
                created_at          TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        async with db.execute("PRAGMA table_info(works)") as cur:
            cols = [r[1] for r in await cur.fetchall()]
        if "rate_snapshot" not in cols:
            await db.execute("ALTER TABLE works ADD COLUMN rate_snapshot REAL")
            await db.execute("""UPDATE works SET rate_snapshot = (
                SELECT price FROM price_list WHERE id = works.price_list_item_id
            ) WHERE rate_snapshot IS NULL""")
            
        await db.commit()
