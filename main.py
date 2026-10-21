# main.py
import logging
import asyncio
from config import BOT_TOKEN

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from DB.database import init_db
from handlers import common, price_list, worker, admin, employer



logging.basicConfig(level=logging.INFO)

dp = Dispatcher()

dp.include_router(common.router) 
dp.include_router(price_list.router)
dp.include_router(worker.router)
dp.include_router(employer.router)

dp.include_router(admin.router)

async def main() -> None:
    await init_db()

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())