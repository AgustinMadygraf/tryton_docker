# Tryton\src\utils\command_utils.py
from ..logs.config_logger import configurar_logging
import time

# Configurar el logger
logger = configurar_logging()

def countdown(seconds, message):
    for i in range(seconds, 0, -1):
        print(f"{message} en {i} segundos...", end="\r")
        time.sleep(1)
    print(" " * 50, end="\r")  # Clear the line after countdown
    logger.info(f"{message} finalizado.")
