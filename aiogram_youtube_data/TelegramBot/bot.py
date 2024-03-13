from asyncio import run
from aiogram import Bot, Dispatcher
from config.config import load_config_telegram_bot



async def main() -> None:
    config = load_config_telegram_bot()
    
    bot = Bot(
        config.telegram_bot.api_key_telegram_bot, 
        parse_mode='HTML')
    
    dp = Dispatcher()
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    run(main())