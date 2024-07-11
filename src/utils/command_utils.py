# Tryton\src\utils\command_utils.py
import time
from src.logs.config_logger import LoggerConfigurator

logger_configurator = LoggerConfigurator()
logger = logger_configurator.get_logger()

def countdown(seconds, message):
    for i in range(seconds, 0, -1):
        print(f"{message} en {i} segundos...", end="\r")
        time.sleep(1)
    print(" " * 50, end="\r")  # Clear the line after countdown
    logger.info(f"{message} finalizado.")
