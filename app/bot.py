import asyncio
from aiogram import Bot, Dispatcher

from app.db.models import async_main
from config import TOKEN
from app.handlers import router
from app.admin import admin


async def main():
    await async_main()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(router, admin) # Роутеры
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
