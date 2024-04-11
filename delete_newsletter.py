from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from functions_db import FunctionsDB
from keyboards import cancellation_kb,newsletter_kb

router = Router()

class Form(StatesGroup):
    keyword_delete = State()

@router.message(F.text == 'Остановить Рассылку')
async def process_stopping(message: Message, state: FSMContext):
    if message.from_user.id != 6619761521:
        await message.answer('Вы не являетесь владельцем бота!')
        return
    await state.set_state(Form.keyword_delete)
    await message.answer('Введите ключевое слово поста, который хотите остановить:',reply_markup=cancellation_kb)

@router.message(Form.keyword_delete)
async def process_stopping(message: Message, state: FSMContext):
    await state.update_data(keyword_delete=message.text)
    data = await state.get_data()
    keyword_delete = data.get('keyword_delete')
    db = FunctionsDB()
    if not db.delete_db(keyword_delete):
        await message.answer('Поста с таким ключевым словом не существует!')
        await state.clear()
        return
    await state.clear()
    await message.answer('Остановка прошла успешно!',reply_markup=newsletter_kb)

