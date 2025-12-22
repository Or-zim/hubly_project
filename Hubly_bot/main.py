import asyncio
import logging

from Hubly_bot.loader import bot, dp

from Hubly_bot.middlewares.auth import AuthMiddleware
from Hubly_bot.handlers.start import router as start_router
from Hubly_bot.handlers.business import router as business_router
from Hubly_bot.handlers.owner import router as owner_router

async def main():
    logging.basicConfig(level=logging.INFO)
    print("🚀 Инициализация Hubly Bot...")

    dp.message.outer_middleware(AuthMiddleware())
    dp.callback_query.outer_middleware(AuthMiddleware())
    dp.my_chat_member.outer_middleware(AuthMiddleware())


    dp.include_router(start_router)
    dp.include_router(business_router)
    dp.include_router(owner_router)

    
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Бот Hubly запущен")
    
    await dp.start_polling(bot)
