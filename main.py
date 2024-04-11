import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
import add_newsletter, delete_newsletter
from config import TOKEN
import router
from functions import newsletters



dp = Dispatcher()




async def main() -> None:
    dp = Dispatcher()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp.include_routers(
        router.router,
        delete_newsletter.router,
        add_newsletter.router,
        )
    
    asyncio.create_task(newsletters())
    await dp.start_polling(bot)




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())







