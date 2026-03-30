# Импортируем asyncio, чтобы запустить асинхронную точку входа.
import asyncio

# Импортируем logging, чтобы видеть служебные сообщения в терминале.
import logging

# Импортируем Bot и Dispatcher из aiogram.
from aiogram import Bot, Dispatcher

# Импортируем класс глобальных настроек бота.
from aiogram.client.default import DefaultBotProperties

# Импортируем режим HTML, чтобы красиво оформлять текст сообщений.
from aiogram.enums import ParseMode

# Импортируем хранилище состояний в оперативной памяти для FSM.
from aiogram.fsm.storage.memory import MemoryStorage

# Импортируем токен бота из конфигурации.
from config import BOT_TOKEN

# Импортируем функцию инициализации базы данных.
from database import init_db

# Импортируем роутер с обработчиками сообщений.
from handlers.student_form import router as student_form_router

# Создаем асинхронную главную функцию запуска проекта.
async def main() -> None:
    # Настраиваем красивый и понятный вывод логов в консоль.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    # Один раз создаем таблицу students перед запуском бота.
    init_db()

    # Создаем объект диспетчера и подключаем к нему память для состояний FSM.
    dispatcher = Dispatcher(storage=MemoryStorage())

    # Подключаем роутер с нашими командами и шагами анкеты.
    dispatcher.include_router(student_form_router)

    # Открываем объект бота через контекстный менеджер, чтобы сессия закрылась аккуратно.
    async with Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    ) as bot:
        # На всякий случай удаляем старый webhook и сбрасываем накопившиеся необработанные обновления.
        await bot.delete_webhook(drop_pending_updates=True)

        # Запускаем long polling и начинаем получать сообщения от Telegram.
        await dispatcher.start_polling(bot)

# Проверяем, что файл запущен напрямую, а не импортирован как модуль.
if __name__ == "__main__":
    # Запускаем асинхронную функцию main внутри стандартного цикла событий Python.
    try:
        asyncio.run(main())

    # Красиво завершаем программу, если пользователь остановил ее вручную.
    except (KeyboardInterrupt, SystemExit):
        # Показываем понятное сообщение в консоли.
        print("Бот остановлен вручную.")