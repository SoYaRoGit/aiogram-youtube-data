import logging
from config.config import load_config_logger



config = load_config_logger()
logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)d #%(levelname)-8s "
    "[%(asctime)s] - %(name)s - %(message)s",
)


# config.logger.path_log
file_handler = logging.FileHandler(
    filename=config.logger.path_log, 
    encoding='utf-8')

file_handler.setFormatter(
    logging.Formatter("%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s")
)

logging.getLogger().addHandler(file_handler)