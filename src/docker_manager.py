"""
tryton_py/src/docker_manager.py
Este módulo se encarga de gestionar Docker y verificar si está instalado y en ejecución.
"""
import subprocess
import time
import shutil
from src.logs.config_logger import LoggerConfigurator

logger_configurator = LoggerConfigurator()
logger = logger_configurator.get_logger()

class DockerManager:
    """Clase para gestionar Docker Desktop."""
    RETRY_COUNT = 3

    def __init__(self):
        self.docker_desktop_path = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"

    def check_docker(self):
        """Verifica si Docker Desktop está instalado."""
        try:
            result = subprocess.run(['docker', '--version'],
                                    check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info("Docker version: %s", result.stdout.decode().strip())
        except subprocess.CalledProcessError as e:
            logger.error("Error verificando Docker: %s", e.stderr.decode().strip())
            raise

    def is_docker_running(self):
        """Verifica si Docker Desktop está en ejecución."""
        try:
            # Verificar si Docker está en el PATH antes de intentar ejecutar el comando
            if not shutil.which('docker'):
                raise FileNotFoundError("Docker no está en el PATH o no está instalado.")

            for _ in range(self.RETRY_COUNT):
                try:
                    subprocess.run(['docker', 'info'], check=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    logger.info("Docker está en ejecución.")
                    return True
                except subprocess.CalledProcessError as e:
                    logger.error("Error verificando el estado de Docker: %s",
                                 e.stderr.decode().strip())
                    return False
        except FileNotFoundError as e:
            logger.error("Archivo no encontrado: %s", str(e))
            return False
        except subprocess.CalledProcessError as e:
            logger.error("Error en el proceso de Docker: %s", str(e))
            return False
        except (OSError, subprocess.SubprocessError) as e:
            logger.error("Error inesperado al verificar Docker: %s", str(e))
            return False

    def start_docker_desktop(self):
        """Inicia Docker Desktop."""
        try:
            logger.info("Iniciando Docker Desktop...")
            subprocess.Popen([self.docker_desktop_path], shell=True)
            time.sleep(30)  # Espera para que Docker Desktop se inicie
            if self.is_docker_running():
                logger.info("Docker Desktop iniciado exitosamente.")
            else:
                logger.error("No se pudo iniciar Docker Desktop.")
        except Exception as e:
            logger.error("Error iniciando Docker Desktop: %s", str(e))
            raise

    def initialize_docker(self):
        """Inicializa Docker y verifica si está en ejecución."""
        self.check_docker()
        if not self.is_docker_running():
            self.start_docker_desktop()
        else:
            logger.info("Docker ya está en ejecución.")
