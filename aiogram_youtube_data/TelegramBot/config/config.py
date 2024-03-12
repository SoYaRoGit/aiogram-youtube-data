from dataclasses import dataclass
from environs import Env



@dataclass
class TelegramBot:
    """Presentation class for telegram bot"""
    api_key_telegram_bot: str


@dataclass
class ConfigTelegramBot:
    """Configuration class for telegram bot"""
    telegram_bot: TelegramBot


def load_config_telegram_bot(path_env: str = '.env' | None) -> ConfigTelegramBot:
    """Telegram bot configuration loading function

    Args:
        path_env (str, optional): Path to the .env file . Defaults to '.env' | None.

    Raises:
        ValueError: API_KEY_TELEGRAM_BOT format is incorrect

    Returns:
        ConfigTelegramBot: Configuration class for telegram bot
    """
    env = Env()
    env.read_env(path_env)
    
    API_KEY_TELEGRAM_BOT = env('API_KEY_TELEGRAM_BOT')
    if not API_KEY_TELEGRAM_BOT or len(API_KEY_TELEGRAM_BOT) != 46:
        raise ValueError(f'Failed to load key API_KEY_TELEGRAM_BOT из {path_env}\nKey: {API_KEY_TELEGRAM_BOT}')
    
    return ConfigTelegramBot(
        telegram_bot=TelegramBot(
            api_key_telegram_bot=API_KEY_TELEGRAM_BOT
        )
    )