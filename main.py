# main.py
import logging
import asyncio
from config import BOT_TOKEN

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from DB.database import init_db
from handlers import common, price, payouts, works, users

from middlewares.user import UserMiddleware
from middlewares.role import RoleMiddleware
from middlewares.permission import PermissionMiddleware



logging.basicConfig(level=logging.INFO)

dp = Dispatcher()

dp.include_router(common.router) 
dp.include_router(price.router)
dp.include_router(works.router)
dp.include_router(payouts.router)
dp.include_router(users.router)


dp.message.middleware(UserMiddleware())
dp.message.middleware(RoleMiddleware())

dp.callback_query.middleware(UserMiddleware())
dp.callback_query.middleware(RoleMiddleware())
dp.callback_query.middleware(PermissionMiddleware())


async def main() -> None:
    await init_db()
    
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())