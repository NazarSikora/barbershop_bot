import asyncio 
from aiogram import Bot, Dispatcher, types
from config import BOT_TOKEN
from database.db import create_tables
from handlers import start

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    await create_tables()

    dp.include_router(start.router)

    print("Бот запущено...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

