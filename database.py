# Импортируем sqlite3, чтобы работать с базой данных SQLite.
import sqlite3

# Импортируем путь к базе данных из файла конфигурации.
from config import DATABASE_PATH

# Создаем функцию для получения нового подключения к базе данных.
def get_connection() -> sqlite3.Connection:
    # Возвращаем подключение к файлу базы данных school_data.db.
    return sqlite3.connect(DATABASE_PATH)

# Создаем функцию инициализации базы данных.
def init_db() -> None:
    # Открываем подключение к базе данных через контекстный менеджер.
    with get_connection() as connection:
        # Создаем курсор, через который будем выполнять SQL-запросы.
        cursor = connection.cursor()

        # Выполняем SQL-запрос на создание таблицы students, если ее еще нет.
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                grade TEXT NOT NULL
            )
            """
        )

        # Сохраняем изменения в базе данных.
        connection.commit()

# Создаем функцию для добавления новой записи о студенте в таблицу students.
def add_student(name: str, age: int, grade: str) -> None:
    # Открываем подключение к базе данных через контекстный менеджер.
    with get_connection() as connection:
        # Создаем курсор для выполнения SQL-запроса на вставку данных.
        cursor = connection.cursor()

        # Выполняем безопасный SQL-запрос с подстановкой значений через параметры.
        cursor.execute(
            "INSERT INTO students (name, age, grade) VALUES (?, ?, ?)",
            (name, age, grade),
        )

        # Сохраняем изменения после добавления записи.
        connection.commit()