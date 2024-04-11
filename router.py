from aiogram import Router,Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import TOKEN
from aiogram.enums import ParseMode
from keyboards import newsletter_kb


router = Router()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if message.from_user.id != 6619761521:
        await message.answer('Вы не являетесь владельцем бота!')
        return
    await message.answer(f"Здравствуйте {message.from_user.full_name}! ", reply_markup=newsletter_kb)
