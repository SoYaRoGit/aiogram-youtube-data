from config.config import load_config_database

class DataBase:
    def __init__(self) -> None:
        config = load_config_database()
        self.__path_database = config.database.path_database