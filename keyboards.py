from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    )

newsletter_kb = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='Добавить Рассылку'),
            KeyboardButton(text='Остановить Рассылку'),
        ],
        [
            KeyboardButton(text='Информация')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)



cancellation_kb = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='Отменить')

        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)