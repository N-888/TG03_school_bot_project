# Импортируем модуль os, чтобы получать значения из переменных окружения.
import os

# Импортируем Path, чтобы удобно работать с путями к файлам и папкам.
from pathlib import Path

# Импортируем функцию load_dotenv, чтобы загрузить переменные из файла .env.
from dotenv import load_dotenv

# Сохраняем путь к папке, где лежит текущий файл config.py.
BASE_DIR = Path(__file__).resolve().parent

# Формируем путь к файлу .env в корне проекта.
ENV_FILE = BASE_DIR / ".env"

# Загружаем переменные окружения из файла .env.
load_dotenv(ENV_FILE)

# Получаем токен бота из переменной окружения BOT_TOKEN и сразу убираем лишние пробелы по краям.
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# Формируем полный путь к базе данных school_data.db.
DATABASE_PATH = BASE_DIR / "school_data.db"

# Проверяем, что токен действительно найден.
if not BOT_TOKEN:
    # Останавливаем программу с понятной ошибкой, если токен не указан.
    raise ValueError("Не найден BOT_TOKEN. Создай файл .env в корне проекта и вставь туда токен от BotFather.")