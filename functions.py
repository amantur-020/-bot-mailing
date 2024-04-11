import re
from aiogram.enums import ParseMode
from config import TOKEN, DESTINATION_CHAT
from aiogram import Bot
from functions_db import FunctionsDB
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio



# Функция для получения ID сообщения из ссылки
def get_telegram_message_id(text: str):
    match = re.search(r'/(\d+)$', text)  
    if match:
        return int(match.group(1))
    else:
        return None

# Функция для отправки постов
async def send_newsletters():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    db = FunctionsDB()

    now = datetime.datetime.now()
    current_minute = now.minute
    message_id=db.get_message_id_by_time(current_minute)
    for chat_id in DESTINATION_CHAT:
        if chat_id is not None and message_id is not None:
            await bot.forward_message(chat_id, '@mdlsg', message_id)



async def newsletters():
    while True:
        now = datetime.datetime.now()
        await asyncio.sleep(60 - now.second)
        await send_newsletters()




