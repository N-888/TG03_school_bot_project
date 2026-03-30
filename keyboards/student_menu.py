# Импортируем KeyboardButton, чтобы создавать кнопки в обычной клавиатуре Telegram.
from aiogram.types import KeyboardButton

# Импортируем ReplyKeyboardMarkup, чтобы собирать клавиатуру из кнопок.
from aiogram.types import ReplyKeyboardMarkup

# Создаем функцию для основной клавиатуры бота.
def get_main_keyboard() -> ReplyKeyboardMarkup:
    # Возвращаем готовую клавиатуру с основными действиями.
    return ReplyKeyboardMarkup(
        # Описываем кнопки по строкам.
        keyboard=[
            # В первой строке размещаем кнопку начала анкеты.
            [KeyboardButton(text="📝 Заполнить анкету")],

            # Во второй строке размещаем кнопку помощи и кнопку отмены.
            [
                KeyboardButton(text="ℹ️ Помощь"),
                KeyboardButton(text="❌ Отмена"),
            ],
        ],

        # Делаем клавиатуру компактнее на экране телефона и компьютера.
        resize_keyboard=True,

        # Показываем подсказку в поле ввода.
        input_field_placeholder="Выбери действие ниже 👇",
    )

# Создаем функцию для клавиатуры во время заполнения анкеты.
def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    # Возвращаем клавиатуру только с одной кнопкой отмены.
    return ReplyKeyboardMarkup(
        # Размещаем кнопку отмены на одной строке.
        keyboard=[[KeyboardButton(text="❌ Отмена")]],

        # Делаем клавиатуру компактнее.
        resize_keyboard=True,

        # Показываем подсказку в поле ввода, чтобы пользователь понял, что можно прервать действие.
        input_field_placeholder="Введи ответ или нажми «Отмена» ✍️",
    )