# Импортируем State, чтобы описывать отдельные шаги анкеты.
from aiogram.fsm.state import State

# Импортируем StatesGroup, чтобы объединить шаги анкеты в одну группу состояний.
from aiogram.fsm.state import StatesGroup

# Создаем класс состояний анкеты студента.
class StudentForm(StatesGroup):
    # Создаем состояние, в котором бот ждет имя пользователя.
    name = State()

    # Создаем состояние, в котором бот ждет возраст пользователя.
    age = State()

    # Создаем состояние, в котором бот ждет класс пользователя.
    grade = State()