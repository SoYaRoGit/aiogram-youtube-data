# Импортируем необходимые модули и объекты
from asyncio import run
from aiogram import Dispatcher
from config.config import bot
from handlers.handler import handler_router
from keyboards.set_menu import set_main_menu
from utils.logger import logger


# Инициализируем журналирование с информационным сообщением о запуске бота
logger.info('Starting bot')

# Определяем главную функцию для запуска бота
async def main() -> None:
    """
    Основная функция для запуска бота.
    """
    # Создаем экземпляр диспетчера для обработки входящих обновлений
    dp = Dispatcher()
    
    # Включаем роутер обработчиков сообщений
    dp.include_router(handler_router)
    
    # Устанавливаем основное меню команд
    await set_main_menu(bot)
    
    # Удаляем вебхук и начинаем опрос обновлений от Telegram
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Проверяем, выполняется ли скрипт как основной модуль
if __name__ == '__main__':
    # Запускаем основную функцию с помощью asyncio.run
    run(main())