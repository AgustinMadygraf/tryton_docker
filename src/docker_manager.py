"""
tryton_py/src/docker_manager.py
Este módulo se encarga de gestionar Docker y verificar si está instalado y en ejecución.
"""
import subprocess
import time
import shutil
from .utils.command_utils import countdown
from src.logs.config_logger import LoggerConfigurator

logger_configurator = LoggerConfigurator()
logger = logger_configurator.get_logger()

class DockerManager:
    RETRY_COUNT = 3

    def __init__(self):
        self.docker_desktop_path = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"

    def check_docker(self):
        try:
            result = subprocess.run(['docker', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info(f"Docker version: {result.stdout.decode().strip()}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error verificando Docker: {e.stderr.decode().strip()}")
            raise

    def is_docker_running(self):
        """Verifica si Docker Desktop está en ejecución."""
        try:
            # Verificar si Docker está en el PATH antes de intentar ejecutar el comando
            if not shutil.which('docker'):
                raise FileNotFoundError("Docker no está en el PATH o no está instalado.")

            for _ in range(self.RETRY_COUNT):
                try:
                    result = subprocess.run(['docker', 'info'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    logger.info("Docker está en ejecución.")
                    return True
                except subprocess.CalledProcessError as e:
                    logger.error(f"Error verificando el estado de Docker: {e.stderr.decode().strip()}")
                    return False
        except Exception as e:
            logger.error(f"Excepción al verificar Docker: {str(e)}")
            return False

    def start_docker_desktop(self):
        try:
            logger.info("Iniciando Docker Desktop...")
            subprocess.Popen([self.docker_desktop_path], shell=True)
            time.sleep(30)  # Espera para que Docker Desktop se inicie
            if self.is_docker_running():
                logger.info("Docker Desktop iniciado exitosamente.")
            else:
                logger.error("No se pudo iniciar Docker Desktop.")
        except Exception as e:
            logger.error(f"Error iniciando Docker Desktop: {str(e)}")
            raise

    def initialize_docker(self):
        """Inicializa Docker y verifica si está en ejecución."""
        self.check_docker()
        if not self.is_docker_running():
            self.start_docker_desktop()
        else:
            logger.info("Docker ya está en ejecución.")