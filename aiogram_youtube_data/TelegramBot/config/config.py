from aiogram import Bot
from dataclasses import dataclass
from environs import Env
from pathlib import Path


@dataclass
class TelegramBot:
    """Презентационный класс для телеграм-бота"""
    api_key_telegram_bot: str


@dataclass
class ConfigTelegramBot:
    """Класс конфигурации для Telegram-бота"""
    telegram_bot: TelegramBot


def load_config_telegram_bot(path_env: str = '.env') -> ConfigTelegramBot:
    """Функция загрузки конфигурации бота Telegram

    Аргументы:
        path_env (str): путь к файлу .env. По умолчанию «.env»

    Поднимает:
        ValueError: неверный формат API_KEY_TELEGRAM_BOT

    Возврат:
        ConfigTelegramBot: класс конфигурации для бота Telegram.
    """
    validate_env_file(path_env)
    
    env = Env()
    env.read_env(path_env)
    
    API_KEY_TELEGRAM_BOT: str = env.str('API_KEY_TELEGRAM_BOT')
    if not API_KEY_TELEGRAM_BOT or len(API_KEY_TELEGRAM_BOT) != 46:
        # logger.error(f'Произошла ошибка при инициализации API_KEY_TELEGRAM_BOT из {path_env}\nКлюч: {API_KEY_TELEGRAM_BOT}')
        raise ValueError(f'Произошла ошибка при инициализации API_KEY_TELEGRAM_BOT из {path_env}\nКлюч: {API_KEY_TELEGRAM_BOT}')
    
    return ConfigTelegramBot(
        telegram_bot=TelegramBot(
            api_key_telegram_bot=API_KEY_TELEGRAM_BOT
        )
    )


@dataclass
class ServiceYouTubeV3:
    """Класс представления для ServiceYouTubeV3"""
    api_key_service_youtube_v3: str


@dataclass
class ConfigServiceYouTubeV3:
    """Класс конфигурации для ServiceYouTubeV3"""
    service_youtube: ServiceYouTubeV3


def load_config_service_youtube(path_env: str = '.env'):
    """Функция загрузки конфигурации ServiceYouTubeV3

    Аргументы:
        path_env (str): путь к файлу .env. По умолчанию «.env»

    Поднимает:
        ValueError: неверный формат API_KEY_SERVICE_YOUTUBE

    Возврат:
        ConfigServiceYouTubeV3: класс конфигурации для ServiceYouTubeV3.
    """
    validate_env_file(path_env)  

    env = Env()
    env.read_env(path_env)
    
    API_KEY_SERVICE_YOUTUBE: str = env.str('API_KEY_SERVICE_YOUTUBE')
    if not API_KEY_SERVICE_YOUTUBE or len(API_KEY_SERVICE_YOUTUBE) != 39:
        #logger.error(f'Произошла ошибка при инициализации API_KEY_SERVICE_YOUTUBE из {path_env}\nКлюч: {API_KEY_SERVICE_YOUTUBE}')
        raise ValueError(f'Произошла ошибка при инициализации API_KEY_SERVICE_YOUTUBE из {path_env}\nКлюч: {API_KEY_SERVICE_YOUTUBE}')
    
    return ConfigServiceYouTubeV3(
        service_youtube=ServiceYouTubeV3(
            api_key_service_youtube_v3=API_KEY_SERVICE_YOUTUBE
        )
    )
    

@dataclass
class Logger:
    path_log: str


@dataclass 
class ConfigLogger:
    logger: Logger


def load_config_logger(path_env: str = '.env') -> ConfigLogger:
    validate_env_file(path_env)
    
    env = Env()
    env.read_env(path_env)
    
    PATH_LOG: str = env.str('PATH_LOG')
    path_log_obj = Path(PATH_LOG)
    
    
    if not path_log_obj.name == 'bot.log':
        # logger.error(f'Имя файла в path_log должно быть bot.log | Имя файла: {path_log_obj.name}')
        raise ValueError(f'Имя файла в path_log должно быть bot.log | Имя файла: {path_log_obj.name}')
    
    return ConfigLogger(
        logger=Logger(
            path_log=PATH_LOG
        )
    )


@dataclass
class DataBase:
    path_database: str


@dataclass
class ConfigDataBase:
    database: DataBase


def __validate_database_path(path: str) -> None:
    if path is None:
        # logger.error('Переменная PATH_DATABASE не определена в файле окружения')
        raise ValueError("Переменная PATH_DATABASE не определена в файле окружения")
    
    valid_extensions = ('.db', '.sqlite3')
    if not (isinstance(path, str) and
            path.strip() != '' and
            path.index('.') > 0 and
            not path.startswith('.') and
            path.endswith(valid_extensions)):
        # logger.error("Некорректный путь к базе данных. Ожидается строка, заканчивающаяся на '.db' или '.sqlite3'")
        raise ValueError("Некорректный путь к базе данных. Ожидается строка, заканчивающаяся на '.db' или '.sqlite3'")


def __create_database_file(path: str) -> None:
    database_path_obj = Path(path)
    if not database_path_obj.is_file():
        database_path_obj.touch()


def load_config_database(path_env: str = '.env') -> ConfigDataBase:
    validate_env_file(path_env)
    
    env = Env()
    env.read_env(path_env)
    
    PATH_DATABASE = env.str('PATH_DATABASE')
    __validate_database_path(PATH_DATABASE)
    __create_database_file(PATH_DATABASE)
    
    return ConfigDataBase(database=DataBase(path_database=PATH_DATABASE))


def validate_env_file(path_env: str) -> None:
    """Проверяет наличие файла .env и допустимое имя"""
    path_env_obj = Path(path_env)
    if not path_env_obj.exists():
        # logger.error(f"Файл .env по адресу {path_env} не существует. Укажите действительный путь к файлу .env")
        raise ValueError(f"Файл .env по адресу {path_env} не существует. Укажите действительный путь к файлу .env")
    if not path_env_obj.is_file():
        # logger.error(f"Указанный путь {path_env} не является файлом. Укажите правильный путь к файлу .env")
        raise ValueError(f"Указанный путь {path_env} не является файлом. Укажите правильный путь к файлу .env")
    if not path_env_obj.name == '.env':
        # logger.error(f"Имя файла в path_env должно быть .env | Имя файла: {path_env_obj.name}")
        raise ValueError(f"Имя файла в path_env должно быть .env | Имя файла: {path_env_obj.name}")
    
    
config = load_config_telegram_bot()
    
bot = Bot(
    config.telegram_bot.api_key_telegram_bot, 
    parse_mode='HTML')