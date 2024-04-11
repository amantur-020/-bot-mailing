from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from functions import get_telegram_message_id,newsletters
from functions_db import FunctionsDB
from keyboards import cancellation_kb,newsletter_kb
import asyncio
from aiogram.filters import Command


router = Router()

class Form(StatesGroup):
    keyword = State()
    message_id = State()
    time = State()





@router.message((F.text == 'Добавить Рассылку'))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    if message.from_user.id != 6619761521:
        await message.answer('Вы не являетесь владельцем бота!')
        return
    await state.set_state(Form.keyword)
    await message.answer("Придумайте ключевое слово для этой рассылки. В дальнейшем вы сможете остановить эту рассылку при помощи этого слова",reply_markup=cancellation_kb)

@router.message(F.text == 'Отменить')
async def cancel_process(message:Message,state:FSMContext):
    await state.clear()
    await message.answer('Вы вышли в главную страницу',reply_markup=newsletter_kb)


@router.message(Form.keyword)
async def process_keyword(message: Message, state: FSMContext) -> None:
    await state.update_data(keyword=message.text.lower())
    await state.set_state(Form.message_id)
    await message.answer('Теперь отправьте ссылку поста:')

@router.message(Form.message_id)
async def process_message_id(message: Message, state: FSMContext) -> None:
    if not get_telegram_message_id(message.text):
        await message.answer('Некорректная ссылка.\nУбедитесь что вы скинули ссылку\nЧтобы повторно скинуть ссылку нажмите на кнопку Отменить')
        return 
    await state.update_data(message_id=get_telegram_message_id(message.text))
    await state.set_state(Form.time)
    await message.answer('Теперь введите минуту часа:')


@router.message(Form.time)
async def process_time(message: Message, state: FSMContext) -> None:
    try:
        await state.update_data(time=message.text)
    except Exception:
        await message.answer('Некорректное минута')
        return
    data = await state.get_data()
    keyword = data.get('keyword')
    message_id = data.get('message_id')
    time = data.get('time')
    db = FunctionsDB()
    db.create_db()
    db.add_db(keyword, message_id, time)

    await message.answer('Рассылка успешно добавлено',reply_markup=newsletter_kb)
    await state.clear()



@router.message(Command('start_newletters'))
async def start_newletters(message:Message):
    if message.from_user.id != 6619761521:
        await message.answer('Вы не являетесь владельцем бота!')
        return
    try:
        asyncio.create_task(newsletters())
        await message.answer('Рассылка успешно работает!',reply_markup=newsletter_kb)
    except Exception:
        await message.answer('Что-то пошло не так попробуйте снова!',reply_markup=newsletter_kb)    



@router.message(F.text == 'Информация')
async def info_process(message:Message):
    if message.from_user.id != 6619761521:
        await message.answer('Вы не являетесь владельцем бота!')
        return
    db=FunctionsDB()
    await message.answer(f'Кол-во активных рассылок: {db.get_record_count()}',reply_markup=newsletter_kb)



@router.message()
async def commands(message:Message):
    if message.from_user.id != 6619761521:
        await message.answer('Вы не являетесь владельцем бота!')
        return
    await message.answer('Используйте кнопки',reply_markup=newsletter_kb)