"""
Kino Bot - Asosiy ishga tushirish fayli.

Professional Telegram kino bot (Aiogram 3.x).
"""

from __future__ import annotations

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, DB_PATH
from database.db import Database
from handlers.admin import router as admin_router
from handlers.user import router as user_router
from middlewares.subscription import SubscriptionMiddleware
from utils.scheduler import setup_scheduler


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  LOGGING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  BOT SETUP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


async def on_startup(bot: Bot, db: Database) -> None:
    """Bot ishga tushganda."""
    me = await bot.get_me()
    logger.info("Bot ishga tushdi: @%s [%s]", me.username, me.id)
    logger.info("Ma'lumotlar bazasi: %s", db.db_path)


async def on_shutdown(db: Database) -> None:
    """Bot to'xtaganda."""
    await db.close()
    logger.info("Ma'lumotlar bazasi yopildi. Bot to'xtatildi.")


async def main() -> None:
    """Asosiy funksiya."""

    if not BOT_TOKEN:
        logger.error(
            "BOT_TOKEN topilmadi! .env faylini tekshiring. "
            ".env.example faylidan nusxa oling."
        )
        sys.exit(1)

    # Database
    db = Database(DB_PATH)
    await db.connect()
    logger.info("Ma'lumotlar bazasiga ulandi.")

    # Bot
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # Dispatcher
    dp = Dispatcher(storage=MemoryStorage())

    # Middleware
    dp.message.middleware(SubscriptionMiddleware(db))
    dp.callback_query.middleware(SubscriptionMiddleware(db))

    # Routerlar (admin birinchi - filter ustunligi uchun)
    dp.include_router(admin_router)
    dp.include_router(user_router)

    # db ni har bir handler'ga uzatish
    dp["db"] = db

    # Lifecycle
    async def _on_startup() -> None:
        await on_startup(bot, db)
        # Schedulerni ishga tushirish
        scheduler = setup_scheduler(bot)
        dp['scheduler'] = scheduler

    async def _on_shutdown() -> None:
        await on_shutdown(db)

    dp.startup.register(_on_startup)
    dp.shutdown.register(_on_shutdown)

    # Polling
    logger.info("Polling boshlandi...")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot to'xtatildi (Ctrl+C)")
