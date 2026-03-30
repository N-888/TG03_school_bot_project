# Импортируем Router, чтобы собрать обработчики в отдельный модуль.
from aiogram import Router

# Импортируем html, чтобы безопасно подставлять текст пользователя в HTML-сообщения.
from aiogram import html

# Импортируем фильтр F для удобных проверок текста сообщений.
from aiogram import F

# Импортируем командные фильтры /start и /help, /cancel.
from aiogram.filters import Command

# Импортируем отдельный фильтр для команды /start.
from aiogram.filters import CommandStart

# Импортируем контекст состояний FSM.
from aiogram.fsm.context import FSMContext

# Импортируем тип Message для подсказок и правильной типизации.
from aiogram.types import Message

# Импортируем объект для удаления временной клавиатуры при необходимости.
from aiogram.types import ReplyKeyboardRemove

# Импортируем функцию записи данных в базу данных.
from database import add_student

# Импортируем функции создания клавиатур.
from keyboards.student_menu import get_cancel_keyboard

# Импортируем функции создания клавиатур.
from keyboards.student_menu import get_main_keyboard

# Импортируем класс состояний анкеты.
from states.student_form import StudentForm

# Создаем роутер для всех обработчиков этого файла.
router = Router()

# Создаем красивый приветственный текст, который будет показываться на старте.
WELCOME_TEXT = (
    "<b>🎓 Школьный бот-анкетатор</b>\n\n"
    "Привет! Я помогу сохранить данные ученика в базу <b>school_data.db</b>.\n\n"
    "<b>Что я умею:</b>\n"
    "• запрашивать имя;\n"
    "• запрашивать возраст;\n"
    "• запрашивать класс;\n"
    "• сохранять все данные в таблицу <b>students</b>.\n\n"
    "Нажми <b>«📝 Заполнить анкету»</b> или введи команду <b>/form</b>."
)

# Создаем текст помощи, чтобы пользователь понял все основные действия.
HELP_TEXT = (
    "<b>ℹ️ Подсказка по боту</b>\n\n"
    "<b>Команды:</b>\n"
    "• /start — открыть приветствие\n"
    "• /form — начать заполнение анкеты\n"
    "• /help — открыть справку\n"
    "• /cancel — отменить текущее действие\n\n"
    "<b>Что нужно ввести:</b>\n"
    "1. Имя\n"
    "2. Возраст\n"
    "3. Класс\n\n"
    "<b>Примеры класса:</b> 5А, 7Б, 9A, 11"
)

# Обрабатываем команду /start.
@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    # На всякий случай очищаем старое состояние, если пользователь начинал анкету раньше.
    await state.clear()

    # Отправляем приветственное сообщение и основную клавиатуру.
    await message.answer(WELCOME_TEXT, reply_markup=get_main_keyboard())

# Обрабатываем команду /help.
@router.message(Command("help"))
async def command_help(message: Message) -> None:
    # Показываем пользователю подробную справку.
    await message.answer(HELP_TEXT, reply_markup=get_main_keyboard())

# Обрабатываем нажатие кнопки «Помощь».
@router.message(F.text == "ℹ️ Помощь")
async def button_help(message: Message) -> None:
    # Показываем пользователю ту же справку через кнопку.
    await message.answer(HELP_TEXT, reply_markup=get_main_keyboard())

# Обрабатываем команду /form для ручного запуска анкеты.
@router.message(Command("form"))
async def command_form(message: Message, state: FSMContext) -> None:
    # Переводим пользователя в состояние ожидания имени.
    await state.set_state(StudentForm.name)

    # Просим ввести имя и показываем кнопку отмены.
    await message.answer(
        "<b>Шаг 1 из 3</b>\n\nВведите имя ученика 👇",
        reply_markup=get_cancel_keyboard(),
    )

# Обрабатываем нажатие кнопки начала анкеты.
@router.message(F.text == "📝 Заполнить анкету")
async def button_form(message: Message, state: FSMContext) -> None:
    # Переводим пользователя в состояние ожидания имени.
    await state.set_state(StudentForm.name)

    # Просим ввести имя и показываем кнопку отмены.
    await message.answer(
        "<b>Шаг 1 из 3</b>\n\nВведите имя ученика 👇",
        reply_markup=get_cancel_keyboard(),
    )

# Обрабатываем команду /cancel.
@router.message(Command("cancel"))

# Обрабатываем нажатие текстовой кнопки отмены.
@router.message(F.text == "❌ Отмена")
async def command_cancel(message: Message, state: FSMContext) -> None:
    # Получаем текущее состояние пользователя.
    current_state = await state.get_state()

    # Если активного состояния нет, просто сообщаем, что отменять нечего.
    if current_state is None:
        # Отправляем спокойное пояснение пользователю.
        await message.answer(
            "Сейчас нет активного заполнения анкеты 🙂",
            reply_markup=get_main_keyboard(),
        )

        # Завершаем работу обработчика раньше.
        return

    # Очищаем состояние пользователя.
    await state.clear()

    # Сообщаем, что заполнение отменено.
    await message.answer(
        "Заполнение анкеты отменено.\n\nКогда будешь готова, нажми <b>«📝 Заполнить анкету»</b> снова.",
        reply_markup=get_main_keyboard(),
    )

# Обрабатываем ввод имени на первом шаге анкеты.
@router.message(StudentForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    # Берем текст сообщения и удаляем лишние пробелы по краям.
    name = (message.text or "").strip()

    # Проверяем, что имя не слишком короткое.
    if len(name) < 2:
        # Просим пользователя ввести более реалистичное имя.
        await message.answer(
            "Имя должно содержать минимум 2 символа.\n\nПопробуй еще раз 👇",
            reply_markup=get_cancel_keyboard(),
        )

        # Завершаем обработчик, чтобы не переходить к следующему шагу.
        return

    # Сохраняем имя в FSM-память.
    await state.update_data(name=name)

    # Переводим пользователя на следующий шаг анкеты.
    await state.set_state(StudentForm.age)

    # Просим ввести возраст.
    await message.answer(
        f"Отлично, <b>{html.quote(name)}</b> сохранено ✅\n\n<b>Шаг 2 из 3</b>\nВведите возраст ученика числом 👇",
        reply_markup=get_cancel_keyboard(),
    )

# Обрабатываем ввод возраста на втором шаге анкеты.
@router.message(StudentForm.age)
async def process_age(message: Message, state: FSMContext) -> None:
    # Берем текст сообщения и удаляем пробелы по краям.
    age_text = (message.text or "").strip()

    # Проверяем, что пользователь ввел только цифры.
    if not age_text.isdigit():
        # Сообщаем, что возраст нужно вводить числом.
        await message.answer(
            "Возраст нужно вводить только цифрами.\n\nНапример: <b>10</b> или <b>15</b> 👇",
            reply_markup=get_cancel_keyboard(),
        )

        # Завершаем обработчик раньше.
        return

    # Преобразуем текст в целое число.
    age = int(age_text)

    # Проверяем, что возраст находится в разумных пределах.
    if age < 5 or age > 25:
        # Просим ввести более реалистичный возраст ученика.
        await message.answer(
            "Для школьной анкеты возраст должен быть в диапазоне от 5 до 25 лет.\n\nПопробуй еще раз 👇",
            reply_markup=get_cancel_keyboard(),
        )

        # Завершаем обработчик раньше.
        return

    # Сохраняем возраст в FSM-память.
    await state.update_data(age=age)

    # Переводим пользователя на следующий шаг анкеты.
    await state.set_state(StudentForm.grade)

    # Просим ввести класс ученика.
    await message.answer(
        "<b>Шаг 3 из 3</b>\n\nТеперь введи класс ученика 👇\n\n<b>Примеры:</b> 5А, 7Б, 9A, 11",
        reply_markup=get_cancel_keyboard(),
    )

# Обрабатываем ввод класса на третьем шаге анкеты.
@router.message(StudentForm.grade)
async def process_grade(message: Message, state: FSMContext) -> None:
    # Берем текст сообщения и удаляем пробелы по краям.
    grade = (message.text or "").strip().upper()

    # Проверяем, что класс не пустой.
    if not grade:
        # Просим пользователя ввести класс еще раз.
        await message.answer(
            "Класс не должен быть пустым.\n\nНапример: <b>6А</b>, <b>8Б</b> или <b>10</b> 👇",
            reply_markup=get_cancel_keyboard(),
        )

        # Завершаем обработчик раньше.
        return

    # Проверяем, что значение класса не слишком длинное.
    if len(grade) > 10:
        # Просим пользователя ввести более короткое и понятное обозначение класса.
        await message.answer(
            "Класс выглядит слишком длинным.\n\nИспользуй короткий формат, например: <b>5А</b>, <b>9Б</b>, <b>11</b> 👇",
            reply_markup=get_cancel_keyboard(),
        )

        # Завершаем обработчик раньше.
        return

    # Обновляем данные в памяти и сразу получаем весь словарь анкеты.
    data = await state.update_data(grade=grade)

    # Сохраняем данные из анкеты в базу данных SQLite.
    add_student(name=data["name"], age=data["age"], grade=data["grade"])

    # Очищаем состояние после успешного завершения анкеты.
    await state.clear()

    # Отправляем красивое итоговое сообщение пользователю.
    await message.answer(
        "<b>✅ Данные успешно сохранены!</b>\n\n"
        f"<b>Имя:</b> {html.quote(data['name'])}\n"
        f"<b>Возраст:</b> {data['age']}\n"
        f"<b>Класс:</b> {html.quote(data['grade'])}\n\n"
        "Запись добавлена в таблицу <b>students</b> базы <b>school_data.db</b>.",
        reply_markup=get_main_keyboard(),
    )

# Обрабатываем любые другие текстовые сообщения, когда пользователь еще не начал анкету.
@router.message()
async def fallback_message(message: Message) -> None:
    # Подсказываем, что делать дальше, если сообщение не подошло ни под один сценарий.
    await message.answer(
        "Я не поняла это сообщение 🤖\n\nНажми <b>«📝 Заполнить анкету»</b> или используй команды <b>/start</b>, <b>/help</b>, <b>/form</b>.",
        reply_markup=get_main_keyboard(),
    )