# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем .env из корня проекта
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Читаем переменные
BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPER_ADMIN_ID = int(os.getenv("SUPER_ADMIN_ID", "0"))
DB_PATH = Path(os.getenv("DB_PATH", "work_bot.db"))

# Валидация — падаем сразу, а не в момент первого запроса
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в .env")
if SUPER_ADMIN_ID == 0:
    raise RuntimeError("SUPER_ADMIN_ID не задан в .env")