from dataclasses import dataclass
from environs import Env
from pathlib import Path


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
        path_env (str, optional): Path to the .env file. Defaults to '.env' | None.

    Raises:
        ValueError: API_KEY_TELEGRAM_BOT format is incorrect

    Returns:
        ConfigTelegramBot: Configuration class for telegram bot
    """
    if not isinstance(path_env, str) or not path_env:
        raise ValueError(f"You must explicitly specify a non-empty path to the .env file in path_env for correct service configuration | path: {path_env}")
    
    path_env_obj = Path(path_env)
    if not path_env_obj.exists():
        raise ValueError(f"The .env file at {path_env} does not exist. Please provide a valid path to the .env file.")
        
    if not path_env_obj.is_file():
        raise ValueError(f"The specified path {path_env} is not a file. Please provide the correct path to the .env file.")

    if not path_env_obj.name == '.env':
        raise ValueError(f"The file name in env_path should be .env | File name: {path_env_obj.name}")
    
    env = Env()
    env.read_env(path_env)
    
    API_KEY_TELEGRAM_BOT: str = env.str('API_KEY_TELEGRAM_BOT')
    if not API_KEY_TELEGRAM_BOT or len(API_KEY_TELEGRAM_BOT) != 46:
        raise ValueError(f'Failed to load key API_KEY_TELEGRAM_BOT from {path_env}\nKey: {API_KEY_TELEGRAM_BOT}')
    
    return ConfigTelegramBot(
        telegram_bot=TelegramBot(
            api_key_telegram_bot=API_KEY_TELEGRAM_BOT
        )
    )


@dataclass
class ServiceYouTubeV3:
    """Presentation class for ServiceYouTubeV3"""
    api_key_service_youtube_v3: str


@dataclass
class ConfigServiceYouTubeV3:
    """Configuration class for ServiceYouTubeV3"""
    service_youtube: ServiceYouTubeV3


def load_config_service_youtube(path_env: str = '.env' | None):
    """ServiceYouTubeV3 configuration loading function

    Args:
        path_env (str, optional): Path to the .env file. Defaults to '.env' | None.

    Raises:
        ValueError: API_KEY_SERVICE_YOUTUBE format is incorrect

    Returns:
        ConfigServiceYouTubeV3: Configuration class for ServiceYouTubeV3
    """
    if not isinstance(path_env, str) or not path_env:
        raise ValueError(f"You must explicitly specify a non-empty path to the .env file in path_env for correct service configuration | path: {path_env}")
    
    path_env_obj = Path(path_env)
    if not path_env_obj.exists():
        raise ValueError(f"The .env file at {path_env} does not exist. Please provide a valid path to the .env file.")
        
    if not path_env_obj.is_file():
        raise ValueError(f"The specified path {path_env} is not a file. Please provide the correct path to the .env file.")

    if not path_env_obj.name == '.env':
        raise ValueError(f"The file name in env_path should be .env | File name: {path_env_obj.name}")    

    env = Env()
    env.read_env(path_env)
    
    API_KEY_SERVICE_YOUTUBE: str = env.str('API_KEY_SERVICE_YOUTUBE')
    if not API_KEY_SERVICE_YOUTUBE or len(API_KEY_SERVICE_YOUTUBE) != 39:
        raise ValueError(f'Failed to load key API_KEY_SERVICE_YOUTUBE from {path_env}\nKey: {API_KEY_SERVICE_YOUTUBE}')
    
    return ConfigServiceYouTubeV3(
        service_youtube=ServiceYouTubeV3(
            api_key_service_youtube_v3=API_KEY_SERVICE_YOUTUBE
        )
    )