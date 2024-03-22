from asyncio import run
from aiogram import Dispatcher
from config.config import bot
from handlers.handler import handler_router
from utils.logger import logger


logger.info('Starting bot')

async def main() -> None:

    
    dp = Dispatcher()
    dp.include_router(handler_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    run(main()) 